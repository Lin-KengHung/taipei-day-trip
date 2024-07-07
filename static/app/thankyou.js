// model
async function fetchOrderData(orderNumber) {
  const response = await fetch("/api/order/" + orderNumber, {
    method: "GET",
    headers: {
      Authorization: "Bearer " + localStorage.getItem("user_token"),
    },
  });
  const data = await response.json();
  if (data.error) {
    location.href = "/";
  } else {
    console.log(data);
    renderMessage(data.data.status, orderNumber);
    renderFooter();
  }
}
// view
function renderFooter() {
  const footer = document.querySelector("footer");
  footer.style.height =
    window.innerHeight - footer.getBoundingClientRect().top + "px";
}

function renderMessage(status, orderNumber) {
  let result = document.querySelector(".order__result");
  let error = document.querySelector(".order__error");
  if (status === 0) {
    result.innerHTML = "行程預定成功！";
  } else {
    result.innerHTML = "行程預定失敗！";
    error.style.display = "block";
    document.querySelector(".order__note").style.display = "none";
    document.querySelector(".order__number").style.display = "none";
    document.querySelector(".order__alert").style.display = "none";
  }
  document.querySelector(".order__number").innerHTML = orderNumber;
}

// controller
renderFooter();
const orderNumber = location.href.match(/^.+\?number=(.+)$/);
if (orderNumber === null) {
  location.href = "/";
}
fetchOrderData(orderNumber[1]);
