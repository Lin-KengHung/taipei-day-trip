// initialize
let popUpSection = `<section class="popup">
  <div class="popup__background">
    <div class="popup__form">
      <div class="popup__form--decorateor-bar"></div>
      <div class="popup__form--content">
        <h3 class="popup__form--title bold">登入會員帳號</h3>
        <input
          type="text"
          name="name"
          class="popup__form--name body-med"
          style="display: none;"
          placeholder="輸入姓名"
        />
        <input
          type="text"
          name="email"
          class="popup__form--email body-med"
          placeholder="輸入電子信箱"
        />
        <input
          type="password"
          name="password"
          class="popup__form--password body-med"
          placeholder="輸入密碼"
        />
        <div class="popup__form--alert" id="error-state" style="display: none;">
            <img src="/static/images/circle-exclamation-solid.svg"  id="error" alt="alert" />
            <img src="/static/images/circle-check-solid.svg" id="success" alt="success" />      
            <span class="popup__form--alert-message"></span>
        </div>
        <button class="popup__form--send regular">登入帳戶</button>
        <div>
            <span class="body-med popup__form--notice">還沒有帳戶？</span>
            <span class="body-med popup__form--tab-change">點此註冊</span>
        </div>
        
      </div>
    </div>
  </div>
</section>`;
let popUpShowing = false;
let loginState;
let body = document.querySelector("body");
body.insertAdjacentHTML("beforeend", popUpSection);
let userBtn = document.querySelector(".header__btn--user");

checkLoginState();

let popUp = document.querySelector(".popup");
let tabState = "signIn";
let emailInput = document.querySelector(".popup__form--email");
let passwordInput = document.querySelector(".popup__form--password");
let nameInput = document.querySelector(".popup__form--name");
// 切換登入/註冊 or 登出
userBtn.addEventListener("click", (e) => {
  console.log("click登入登出按鈕");
  if (loginState) {
    localStorage.removeItem("user_token");
    location.reload();
  } else {
    let tabChangeBtn = document.querySelector(".popup__form--tab-change");
    if (popUpShowing) {
      popUp.style.display = "none";
      tabChangeBtn.removeEventListener("click", changePupUpState);
      popUpShowing = false;
    } else {
      popUp.style.display = "block";
      tabChangeBtn.addEventListener("click", changePupUpState);
      popUpShowing = true;
    }
  }
});

// 送出資料，註冊或登入
document.querySelector(".popup__form--send").addEventListener("click", (e) => {
  console.log("監聽登入或註冊表單按鈕");
  check = checkInput();
  if (check) {
    let data = {
      email: emailInput.value,
      password: passwordInput.value,
    };

    if (tabState === "signIn") {
      // 登入操作
      let url = "/api/user/auth";
      fetch(url, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          if (data.error) {
            document.querySelector(".popup__form--alert").id = "error-state";
            renderErrorMessage(data.message);
          } else {
            localStorage.setItem("user_token", data.token);
            location.reload();
          }
        });
    } else {
      // 註冊操作
      data.name = nameInput.value;
      let url = "/api/user";
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          if (data.error) {
            renderErrorMessage(data.message);
          } else {
            document.querySelector(".popup__form--alert").id = "success-state";
            renderErrorMessage("註冊成功");
          }
        });
    }
  }
});

function changePupUpState() {
  let title = document.querySelector(".popup__form--title");
  let notice = document.querySelector(".popup__form--notice");
  let sendBtn = document.querySelector(".popup__form--send");
  let tabChangeBtn = document.querySelector(".popup__form--tab-change");
  nameInput.value = "";
  emailInput.value = "";
  passwordInput.value = "";
  if (tabState === "signIn") {
    title.innerHTML = "註冊會員帳號";
    nameInput.style.display = "block";
    sendBtn.innerHTML = "註冊新帳戶";
    notice.innerHTML = "已經有帳戶了？";
    tabChangeBtn.innerHTML = "點此登入";
    tabState = "signUp";
  } else {
    title.innerHTML = "登入會員帳號";
    nameInput.style.display = "none";
    sendBtn.innerHTML = "登入帳戶";
    notice.innerHTML = "還沒有帳戶？";
    tabChangeBtn.innerHTML = "點此註冊";
    tabState = "signIn";
  }
  document.querySelector(".popup__form--alert").style.display = "none";
}

function checkInput() {
  let errorMessage = "";
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!nameInput.value && tabState !== "signIn") {
    errorMessage = "請輸入姓名";
  } else if (!emailInput.value) {
    errorMessage = "請輸入Email";
  } else if (!emailPattern.test(emailInput.value)) {
    errorMessage = "Email格式錯誤";
  } else if (!passwordInput.value) {
    errorMessage = "請輸入密碼";
  } else {
    errorMessage = "";
  }

  if (errorMessage == "") {
    document.querySelector(".popup__form--alert").style.display = "none";
    return true;
  } else {
    document.querySelector(".popup__form--alert").id = "error-state";
    renderErrorMessage(errorMessage);
    return false;
  }
}

function renderErrorMessage(errorMessage) {
  document.querySelector(".popup__form--alert-message").innerHTML =
    errorMessage;
  document.querySelector(".popup__form--alert").style.display = "block";
}

function checkLoginState() {
  console.log("進入checkLoginState函數");
  if (localStorage.getItem("user_token")) {
    url = "/api/user/auth";
    fetch(url, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("user_token"),
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("收到fetch user的資料");
        //特殊改token的情況
        if (data.error) {
          console.log("無效token");
          logout();
          location.href = "/";
        } else {
          console.log("現在是登入狀態");
          login();
        }
      });
  } else {
    console.log("現在是登出狀態");
    logout();
  }
  console.log("進入checkLoginState的尾巴");
}

function login() {
  userBtn.innerText = "登出系統";
  loginState = true;
}

function logout() {
  localStorage.removeItem("user_token");
  userBtn.innerText = "登入/註冊";
  loginState = false;
}
