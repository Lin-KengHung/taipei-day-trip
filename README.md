# [Taipei Day Trip](https://taipei1daytrip.store/)

**台北一日遊是一個電商網站，您可以搜尋台北景點，預定行程，並使用信用卡付款**
1. 透過景點名稱、捷運站名稱或關鍵字，取得詳細景點資訊。
2. 透過關鍵字搜尋功能，取得特定景點搜尋結果。
3. 滾動式呈現景點資訊 (paging)
4. 景點圖片的預載與過場動畫
5. 透過 **TapPay** 金流服務，完成付款，取得訂單編號。

**測試帳號**

+ 帳號：test@test.com
+ 密碼：test
+ 手機號碼：0912345678
+ 卡片號碼：4242 4242 4242 4242
+ 過期時間：12/24 （有效期間內即可）
+ 驗證密碼：123

## 功能
+ 滾輪往下滑，可以閱覽所有景點資訊(12筆資料為1頁)，也可以用關鍵字搜尋景點標題
![螢幕擷取畫面 2024-09-17 165058](https://github.com/user-attachments/assets/c2172f18-8045-477e-bf6f-c627154bc35a)
+ 使用者可以註冊、登入、登出網站系統
![螢幕擷取畫面 2024-09-17 165136](https://github.com/user-attachments/assets/5416fd44-17fd-465a-a4d4-cd6e127eb71c)
+ 使用者可以進入各個景點分頁，瀏覽景點資訊並預定行程
![螢幕擷取畫面 2024-09-17 165302](https://github.com/user-attachments/assets/363d3f32-b8a4-4390-a91b-b1260217a39b)
+ 使用者可以對預定行程使用信用卡付款
![螢幕擷取畫面 2024-09-17 171548](https://github.com/user-attachments/assets/88999e2c-c073-46aa-aee3-98c455850079)



## 技術
- **Python** / **FastAPI**：後端框架。
- **JWT**：使用者登入驗證。
- **RESTful API & MVC** 架構，保持程式碼的可維護性與擴展性。
- **TapPay SDK**：第三方金流支付。
- **MySQL**：使用3NF正規化設計，確保資料一致性。
- **Git** / **GitHub**：版本控管，並遵守Git Flow 開發流程。
- **AWS EC2**：雲端部屬。
- **Docker** / **Docker-Compose**：確保本地與雲端環境一致。
- **Nginx**：反向代理伺服器。
- **Let's Encrypt**：提供 SSL 證書，確保 HTTPS 安全連線。


## 系統架構
![taipei-dy-trip 架構圖](https://github.com/user-attachments/assets/bc7ae3a1-08b5-4896-9958-d2342ab4053d)
1. 透過 Git Flow 的方式開發，確保各個版本的控制
2. 主程式是採用前、後端分離的方式去開發，前端使用 HTML、CSS、JavaScript，後端使用 Python FastAPI ，並採用 MVC 架構去設計
3. 資料庫使用 MySQL，儲存會員資料、景點資料、預定資料、訂單資料，部屬在AWS RDS上
4. 當用戶連線到伺服器時，會透過 NGINX 反向代理，自動將連線升級為 HTTPS，確保所有資料傳輸的安全性。

## 資料庫架構
![Taipei_day_trip 資料庫](https://github.com/user-attachments/assets/b686c733-8af7-4165-9781-42b7e8ddcf78)
+ attractions 景點資訊
+ image 景點圖片
+ user 使用者資訊
+ booking 預定資訊 (購物車)
+ purchase 訂單資訊 
+ payment 付款資訊

