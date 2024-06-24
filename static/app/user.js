// Model
class User {
  constructor() {
    this.isLogin = false;
  }
  login(name, email, id) {
    this.isLogin = true;
    this.name = name;
    this.email = email;
    this.id = id;
  }
  logout() {
    localStorage.removeItem("user_token");
    location.reload();
  }
  async getCurrentUser() {
    if (localStorage.getItem("user_token")) {
      document.querySelector(".header__btn--user").innerText = "登出系統";
      try {
        let url = "/api/user/auth";
        let response = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("user_token"),
          },
        });
        let data = await response.json();
        //特殊修改token或是過期的情況
        if (data.error) {
          this.logout();
        } else {
          this.login(data.data.name, data.data.email, data.data.id);
        }
      } catch (error) {
        console.error("沒抓到/api/user/auth的資料", error);
      }
    }
  }
  static async createUser() {
    let user = new User();
    await user.getCurrentUser();
    return user;
  }
}
function verifyInputFormat() {
  let message;
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!nameInput.value && !popUp.isSignInForm) {
    message = "請輸入姓名";
  } else if (!emailInput.value) {
    message = "請輸入Email";
  } else if (!emailPattern.test(emailInput.value)) {
    message = "Email格式錯誤";
  } else if (!passwordInput.value) {
    message = "請輸入密碼";
  } else {
    message = "ok";
  }
  return message;
}
// View
function renderInit() {
  const popUpSection = `<section class="popup">
    <div class="popup__background">
      <div class="popup__form">
        <div class="popup__form--decorateor-bar">
              <img
              class="popup__form--close"
              src="/static/images/close.png"
              alt="close"
            />
        </div>
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
  document.querySelector("body").insertAdjacentHTML("beforeend", popUpSection);
}
class PopupMenuState {
  constructor() {
    this.isSignInForm = true;
    this.element = document.querySelector(".popup");
  }

  hide() {
    this.element.style.display = "none";
  }
  show() {
    this.element.style.display = "block";
    if (!this.isSignInForm) {
      renderForm("signin");
      popUp.isSignInForm = true;
    }
  }
}
function renderForm(format) {
  let title = document.querySelector(".popup__form--title");
  let sendBtn = document.querySelector(".popup__form--send");
  let notice = document.querySelector(".popup__form--notice");
  let tabChangeBtn = document.querySelector(".popup__form--tab-change");
  if (format === "signin") {
    title.innerHTML = "登入會員帳號";
    nameInput.style.display = "none";
    sendBtn.innerHTML = "登入帳戶";
    notice.innerHTML = "還沒有帳戶？";
    tabChangeBtn.innerHTML = "點此註冊";
  } else {
    title.innerHTML = "註冊會員帳號";
    nameInput.style.display = "block";
    sendBtn.innerHTML = "註冊新帳戶";
    notice.innerHTML = "已經有帳戶了？";
    tabChangeBtn.innerHTML = "點此登入";
  }
  document.querySelector(".popup__form--alert").style.display = "none";
}
function renderFormMessage(message) {
  document.querySelector(".popup__form--alert-message").innerHTML = message;
  document.querySelector(".popup__form--alert").style.display = "block";
}

// Controller
// initial render
renderInit();
// overall element
let emailInput = document.querySelector(".popup__form--email");
let passwordInput = document.querySelector(".popup__form--password");
let nameInput = document.querySelector(".popup__form--name");

// instance popUP obj and user obj
let popUp = new PopupMenuState();
let user = await User.createUser();
export { user, popUp };

// listen login/logout btn
document.querySelector(".header__btn--user").addEventListener("click", (e) => {
  if (user.isLogin) {
    // 登出
    user.logout();
  } else {
    popUp.show();
  }
});

// listen form close btn
document.querySelector(".popup__form--close").addEventListener("click", (e) => {
  popUp.hide();
});
// listen switch signin / signup btn
document
  .querySelector(".popup__form--tab-change")
  .addEventListener("click", (e) => {
    if (popUp.isSignInForm) {
      renderForm("signup");
      popUp.isSignInForm = false;
    } else {
      renderForm("signin");
      popUp.isSignInForm = true;
    }
  });
// listen sending data btn and send data
document.querySelector(".popup__form--send").addEventListener("click", (e) => {
  let resultMessage = verifyInputFormat();
  document.querySelector(".popup__form--alert").id = "error-state";
  if (resultMessage === "ok") {
    let data = {
      email: emailInput.value,
      password: passwordInput.value,
    };

    if (popUp.isSignInForm) {
      // 登入操作
      try {
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
              renderFormMessage(data.message);
            } else {
              localStorage.setItem("user_token", data.token);
              location.reload();
            }
          });
      } catch (error) {
        console.error("沒辦法登入/api/user/auth", error);
      }
    } else {
      // 註冊操作
      try {
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
              renderFormMessage(data.message);
            } else {
              document.querySelector(".popup__form--alert").id =
                "success-state";
              renderFormMessage("註冊成功");
            }
          });
      } catch (error) {
        console.error("沒辦法註冊/api/user", error);
      }
    }
  } else {
    renderFormMessage(resultMessage);
  }
});

// redirect to home page
let webTilte = document.querySelector(".header__title");
webTilte.addEventListener("click", (e) => {
  location.href = "/";
});

// redirect to booking page
document
  .querySelector(".header__btn--booking")
  .addEventListener("click", (e) => {
    if (user.isLogin) {
      location.href = "/booking";
    } else {
      popUp.show();
    }
  });
