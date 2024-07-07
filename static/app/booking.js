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
      return data.data;
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

async function makeOrderData(data, prime) {
  const name = document.querySelector(".contact__input--name").value;
  const email = document.querySelector(".contact__input--email").value;
  const phone = document.querySelector(".contact__input--phone").value;
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  const phonePattern = /^09\d{8}$/;
  if (name === "" || !emailPattern.test(email) || !phonePattern.test(phone)) {
    renderErrorMessage("聯絡資料有誤！！");
    return null;
  }
  let orderData = {
    prime: prime,
    order: {
      price: data.price,
      trip: {
        attraction: {
          id: data.attraction.id,
          name: data.attraction.name,
          address: data.attraction.address,
          image: data.attraction.image,
        },
        date: data.date,
        time: data.time,
      },
      contact: {
        name: name,
        email: email,
        phone: phone,
      },
    },
  };
  return orderData;
}

async function submitPayment(orderData) {
  fetch("/api/orders", {
    method: "POST",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("user_token"),
      "Content-Type": "application/json",
    },
    body: JSON.stringify(orderData),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data.data);
      location.href = "/thankyou?number=" + data.data.number;
    });
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
function renderErrorMessage(message) {
  const errorTag = document.querySelector(".confirm__error");
  errorTag.style.display = "block";
  errorTag.innerHTML = message;
}

// Controller
const bookingData = await init();
document
  .querySelector(".booking__delete-icon")
  .addEventListener("click", deleteSchedule);

// TapPay
const APP_ID = 151606;
const APP_KEY =
  "app_hY0PEmHeWIv6aNkxMMDHyGc0LOPEMkow6DajSxmruckTuK5cKTatNQYCRsau";
TPDirect.setupSDK(APP_ID, APP_KEY, "sandbox");
let fields = {
  number: {
    // css selector
    element: "#card-number",
    placeholder: "**** **** **** ****",
  },
  expirationDate: {
    // DOM object
    element: document.getElementById("card-expiration-date"),
    placeholder: "MM / YY",
  },
  ccv: {
    element: "#card-ccv",
    placeholder: "ccv",
  },
};
TPDirect.card.setup({
  fields: fields,
  styles: {
    // Style all elements
    input: {
      color: "gray",
    },
    // Styling ccv field
    "input.ccv": {
      "font-size": "16px",
    },
    // Styling expiration-date field
    "input.expiration-date": {
      "font-size": "16px",
    },
    // Styling card-number field
    "input.card-number": {
      "font-size": "16px",
    },
    // style focus state
    // ":focus": {
    //   color: "black",
    // },
    // style valid state
    ".valid": {
      color: "green",
    },
    // style invalid state
    ".invalid": {
      color: "red",
    },
  },
});

// 送出訂購資訊
let orderNumber = null;
document
  .querySelector("button.confirm__btn")
  .addEventListener("click", async (e) => {
    e.preventDefault();
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    console.log(tappayStatus);
    if (tappayStatus.canGetPrime === false) {
      renderErrorMessage("付款資料有誤！！");
      return;
    }

    TPDirect.card.getPrime(async (result) => {
      if (result.status !== 0) {
        alert("get prime error " + result.msg + result.status);
        return;
      }
      const orderData = await makeOrderData(bookingData, result.card.prime);
      if (orderData === null) {
        console.log("聯絡資料有錯");
      } else {
        console.log(orderData);
        submitPayment(orderData);
      }
    });
  });
