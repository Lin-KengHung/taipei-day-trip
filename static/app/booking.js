import { user } from "./user.js";
// Model
async function init() {
  try {
    const url = "/api/booking";
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("user_token"),
      },
    });
    if (response.status === 403) {
      location.href = "/";
    }
    const data = await response.json();
    if (data.error) {
      renderNoBooking();
    } else {
      renderMain(data.data);
    }
  } catch (error) {
    console.error("沒有成功get /api/booking", error);
  }
}
async function deleteSchedule() {
  try {
    const url = "/api/booking";
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("user_token"),
      },
    });
    const data = await response.json();
    if (data.ok) {
      location.reload();
    }
  } catch (error) {
    console.error("沒有成功delete /api/booking", error);
  }
}
// View
function renderMain(data) {
  document.querySelector("main").style.visibility = "visible";
  document.querySelector(".welcome__username").innerHTML = user.name;
  document.querySelector(".infor__data--attraction-name").innerHTML =
    data.attraction.name;
  document.querySelector(".infor__data--date").innerHTML = data.date;
  const time = document.querySelector(".infor__data--time");
  if (data.time === "morning") {
    time.innerHTML = "08:00-12:00";
  } else {
    time.innerHTML = "14:00-18:00";
  }
  document.querySelector(".infor__data--cost").innerHTML = data.price;
  document.querySelector(".infor__data--address").innerHTML =
    data.attraction.address;
  document.querySelector(".booking__profile--img").src = data.attraction.image;
  document.querySelector(".contact__input--name").placeholder = user.name;
  document.querySelector(".contact__input--email").placeholder = user.email;
  document.querySelector(".confirm__total--cost").innerHTML = data.price;
}
function renderNoBooking() {
  document.querySelector(".welcome__username").innerHTML = user.name;
  document.querySelector("main").style.display = "none";
  document.querySelector("section.empty").style.display = "flex";
  const footer = document.querySelector("footer");
  footer.style.height =
    window.innerHeight - footer.getBoundingClientRect().top + "px";
}

// Controller
init();

document
  .querySelector(".booking__delete-icon")
  .addEventListener("click", deleteSchedule);
