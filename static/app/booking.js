import user from "./user.js";
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
    const data = await response.json();
    renderMain(data.data);
  } catch (error) {
    console.error("沒有成功get /api/booking", error);
  }
}
// View
function renderMain(data) {
  document.querySelector(".booking__username").innerHTML = user.name;
  document.querySelector(".infor__data--attraction-name").innerHTML =
    data.attraction.name;
  document.querySelector(".infor__data--date").innerHTML = data.date;
  document.querySelector(".infor__data--cost").innerHTML = data.price;
  document.querySelector(".infor__data--address").innerHTML =
    data.attraction.address;
  document.querySelector(".booking__profile--img").src = data.attraction.image;
  document.querySelector(".contact__input--name").placeholder = user.name;
  document.querySelector(".contact__input--email").placeholder = user.email;
}
// Controller
init();
document
  .querySelector(".booking__delete-icon")
  .addEventListener("click", (e) => {
    console.log("test");
  });
