const href = location.href;
const pattern = /^http:.+\/attraction\/(\d+)$/;
const attractionID = href.match(pattern)[1];
let time = "morning";
let price = 2000;
let showingImgID = 0;
// --------------------render main page--------------------
renderAttraction(attractionID).then((data) => {
  // --------------------update showing image when click img NO. circle--------------------
  let imageCircles = document.querySelectorAll("input.profile__imgNo--input");
  imageCircles.forEach((circle) => {
    circle.addEventListener("click", (e) => {
      renderNewImg(e.target.id);
    });
  });
  // --------------------update showing image when click arrow button--------------------
  let rightBtn = document.querySelector("img.profile__arrow-btn--right");
  rightBtn.addEventListener("click", (e) => {
    let newImgID;
    if (showingImgID == data.images.length - 1) {
      newImgID = 0;
    } else {
      newImgID = Number(showingImgID) + 1;
    }

    renderNewImg(newImgID);
    let circle = document.getElementById(showingImgID);
    circle.checked = true;
  });
  let leftBtn = document.querySelector("img.profile__arrow-btn--left");
  leftBtn.addEventListener("click", (e) => {
    let newImgID;
    if (showingImgID == 0) {
      newImgID = data.images.length - 1;
    } else {
      newImgID = Number(showingImgID) - 1;
    }
    renderNewImg(newImgID);
    let circle = document.getElementById(showingImgID);
    circle.checked = true;
  });
});

// --------------------redirect to home page--------------------

let webTilte = document.querySelector(".header__title");
webTilte.addEventListener("click", (e) => {
  location.href = "/";
});

// --------------------change price--------------------

let timeRadioInputs = document.querySelectorAll('input[name="time"]');
let priceTag = document.querySelector("span#price");
timeRadioInputs.forEach((timeBtn) => {
  timeBtn.addEventListener("change", (e) => {
    if (timeBtn.id == "morning") {
      price = 2000;
      time = "morning";
    } else {
      price = 2500;
      time = "afternoon";
    }
    priceTag.innerHTML = price;
  });
});

// --------------------send booking information to back-end--------------------

let bookingBtn = document.querySelector("button.form__btn");
bookingBtn.addEventListener("click", (e) => {
  e.preventDefault();
  let date = document.querySelector("input#date").value;
  if (!date) {
    let dateAlert = document.querySelector(".form__alert");
    let formTag = document.querySelector(".profile__content--form");
    formTag.style.height = "322px";
    dateAlert.style.display = "block";
  } else {
    let bookingData = {
      attractionId: Number(attractionID),
      date: date,
      time: time,
      price: price,
    };

    sendBookingData(bookingData);
  }
});
// --------------------function part--------------------

async function renderAttraction(attractionID) {
  // fetch data
  url = "/api/attraction/" + attractionID;
  let response = await fetch(url, { method: "GET" });
  let data = await response.json();
  checkAttractionData(data);

  // 渲染主要頁面
  document.querySelector("h3.profile__content--name").innerHTML =
    data.data.name;
  document.querySelector(".profile__content--cat").innerHTML =
    data.data.category;
  if (data.data.mrt) {
    document.querySelector(".profile__content--mrt").innerHTML =
      "&nbspat&nbsp; " + data.data.mrt;
  }

  document.querySelector(".info__description").innerHTML =
    data.data.description;
  document.querySelector(".info__address").innerHTML = data.data.address;
  document.querySelector(".info__traffic").innerHTML = data.data.transport;

  // 渲染所有圖片並只顯示第一張，只渲染最多10張

  if (data.data.images.length > 11) {
    data.data.images.splice(11);
  }
  let imgBox = document.querySelector("div.profile__image-box");
  for (let i = 0; i < data.data.images.length; i++) {
    let zIndex = 1;
    let opacity = 0;
    if (i == 0) {
      zIndex = 2;
    }
    let imgTag = `<img class="attraction" src="${data.data.images[i]}" id="img${i}" alt="景點圖片" style="z-index: ${zIndex}; opacity: ${opacity};"/>`;
    imgBox.insertAdjacentHTML("beforeend", imgTag);
  }
  let firstImg = document.querySelector(`img#img0`);
  firstImg.style.opacity = 1;
  // 渲染img NO. circle
  addImageNoCircle(data.data.images.length);
  return data.data;
}

function checkAttractionData(data) {
  if (data.error) {
    location.href = "/";
  }
}

function addImageNoCircle(n) {
  let imgNoBox = document.querySelector(".profile__imgNo");
  for (let i = 0; i < n; i++) {
    let circle;
    if (i == 0) {
      circle = `<label class="profile__imgNo--box ">
    <input type="radio" class="profile__imgNo--input" name="imgNo" checked id=${i} />
    <div class="circle" ></div>
  </label>`;
    } else {
      circle = `<label class="profile__imgNo--box ">
      <input type="radio" class="profile__imgNo--input" name="imgNo" id=${i} />
      <div class="circle" ></div>
    </label>`;
    }

    imgNoBox.insertAdjacentHTML("beforeend", circle);
  }
}

function renderNewImg(newImgID) {
  if (newImgID != showingImgID) {
    let oldImg = document.querySelector(`img#img${showingImgID}`);
    let newImg = document.querySelector(`img#img${newImgID}`);
    oldImg.style.zIndex = 1;
    newImg.style.zIndex = 2;
    oldImg.style.opacity = 0;
    newImg.style.opacity = 1;
    showingImgID = Number(newImgID);
  }
}

async function sendBookingData(bookingData) {
  let response = await fetch("/api/booking", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(bookingData),
  });
  let result = await response.json();
  console.log(result);
  return result;
}
