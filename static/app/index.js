let nextPage;
let keyword = "";
let attractionSection = document.querySelector("section.attraction");

// --------------------first render--------------------
renderAttraction(0, "");

// --------------------when users scroll down to the bottom--------------------

const option = {
  root: null,
  rootMargin: "0px 0px 0px 0px",
  threshold: 0.0,
};
const callback = (entries) => {
  if (entries[0].isIntersecting && nextPage != null) {
    renderAttraction(nextPage, keyword);
  }
};
const observer = new IntersectionObserver(callback, option);
let footer = document.querySelector("footer");
observer.observe(footer);

// --------------------keyword search--------------------

let searchBtn = document.querySelector("button.search");
searchBtn.addEventListener("click", (e) => {
  keyword = document.querySelector("input#attraction").value;
  attractionSection.innerHTML = "";
  renderAttraction(0, keyword);
});

// --------------------mrt horizontal scroll bar--------------------
let mrtContainer = document.querySelector("div.mrt-container");
let rightBtn = document.querySelector("img.right-arrow");
let leftBtn = document.querySelector("img.left-arrow");
rightBtn.addEventListener("click", (e) => {
  mrtContainer.scrollLeft += mrtContainer.clientWidth * 0.8;
});
leftBtn.addEventListener("click", (e) => {
  mrtContainer.scrollLeft -= mrtContainer.clientWidth * 0.8;
});

// --------------------mrt search as keyword--------------------

searchKeywordByMRT();

// --------------------function part--------------------

async function renderAttraction(page = 0, keyword = "") {
  url = "/api/attractions?page=" + page;
  if (keyword != "") {
    url += "&keyword=" + keyword;
  }
  let response = await fetch(url, { method: "GET" });
  let data = await response.json();
  nextPage = data.nextPage;
  for (let i = 0; i < data.data.length; i++) {
    let mrt;
    data.data[i].mrt == null ? (mrt = "") : (mrt = data.data[i].mrt);
    addAttractionBoxes(
      data.data[i].images[0],
      data.data[i].name,
      mrt,
      data.data[i].category
    );
  }
}

async function renderMrts() {
  url = "/api/mrts";
  let response = await fetch(url, { method: "GET" });
  let data = await response.json();
  let mrtsContainer = document.querySelector("div.mrt-container");

  for (let i = 0; i < data.data.length; i++) {
    let mrt = `<div class="mrt body-med">${data.data[i]}</div>`;
    mrtsContainer.insertAdjacentHTML("beforeend", mrt);
  }
}

function addAttractionBoxes(imgURL, name, mrt, cat) {
  let box = `<div class="box-outer">
        <div class="box">
            <div class="img-container">
                <img src="${imgURL}" alt="景點圖片" />
            </div>
        <div class="attraction-name body-bold">${name}</div>
        <div class="attraction-info">
            <div class="attraction-mrt">${mrt}</div>
            <div class="attraction-cat">${cat}</div>
        </div>
        </div>
    </div>`;

  attractionSection.insertAdjacentHTML("beforeend", box);
}

async function searchKeywordByMRT() {
  await renderMrts();
  let mrts = document.querySelectorAll("div.mrt");
  mrts.forEach((mrt) => {
    mrt.addEventListener("click", (e) => {
      keyword = mrt.innerHTML;
      attractionSection.innerHTML = "";
      renderAttraction(0, keyword);
      input = document.querySelector("input#attraction");
      input.value = keyword;
    });
  });
}
