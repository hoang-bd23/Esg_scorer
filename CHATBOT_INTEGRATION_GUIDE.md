# 🤖 Hướng dẫn Tích hợp Vertex AI Chatbot lên Website Bất Kỳ

> **Cập nhật:** 2026-04-08

---

## Tổng quan

Tài liệu này hướng dẫn cách tích hợp chatbot AI (Vertex AI / Dialogflow CX) lên **bất kỳ website nào** chỉ với vài dòng HTML, mà không cần thay đổi backend hay cài thêm thư viện.

### Kiến trúc

```
Website của bạn (HTML)
    │
    └── <df-messenger> widget  ← Thêm vào HTML (~15 dòng)
            │
            ▼
        Dialogflow CX API      ← Google quản lý hoàn toàn
            │
            ▼
        Vertex AI Agent         ← Agent bạn đã tạo trên GCP
```

---

## Yêu cầu trước khi bắt đầu

1. **GCP Project** với billing đã bật
2. **Dialogflow CX Agent** đã tạo xong (hoặc Conversational Agent)
3. **Bật Dialogflow CX Messenger integration** trên Agent (xem Bước 1)

---

## Bước 1: Bật Integration trên GCP Console

1. Truy cập [Dialogflow CX Console](https://dialogflow.cloud.google.com/cx/projects) hoặc [Conversational Agents Console](https://conversational-agents.cloud.google.com)
2. Chọn GCP Project → Chọn Agent
3. Vào tab **Manage** → **Integrations** → Click **Connect** trên **Dialogflow CX Messenger**
4. Chọn **Unauthenticated API** (cho phép mọi khách truy cập)
5. (Tùy chọn) Restrict domain — chỉ cho phép website của bạn
6. Click **Enable** → Copy đoạn **embed code**

---

## Bước 2: Nhúng vào Website

### Cách đơn giản nhất (Bất kỳ website HTML nào)

Dán 3 đoạn code sau vào file HTML của bạn:

**Trong `<head>`:**
```html
<!-- CSS cho Dialogflow Messenger -->
<link rel="stylesheet" href="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/themes/df-messenger-default.css">

<!-- JS cho Dialogflow Messenger -->
<script src="https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js"></script>

<!-- CSS tùy chỉnh giao diện -->
<style>
    df-messenger {
        z-index: 999;
        position: fixed;
        --df-messenger-font-color: #000;
        --df-messenger-font-family: Google Sans, sans-serif;
        --df-messenger-chat-background: #f3f6fc;
        --df-messenger-message-user-background: #d3e3fd;
        --df-messenger-message-bot-background: #fff;
        bottom: 16px;
        right: 16px;
    }
</style>
```

**Trước `</body>`:**
```html
<!-- Vertex AI Chatbot Widget -->
<df-messenger
    location="us-central1"
    project-id="YOUR_PROJECT_ID"
    agent-id="YOUR_AGENT_ID"
    language-code="vi"
    max-query-length="-1">
    <df-messenger-chat-bubble
        chat-title="AI Assistant">
    </df-messenger-chat-bubble>
</df-messenger>
```

> ⚠️ Thay `YOUR_PROJECT_ID` và `YOUR_AGENT_ID` bằng giá trị thật từ GCP Console.

---

### Cách dùng cho Jinja2 / FastAPI (Như dự án ESG Scorer)

1. Tạo file `chatbot_embed.html` chứa widget code (xem file mẫu trong `src/esg_scorer/web/templates/`)
2. Trong `base.html`, thêm: `{% include 'chatbot_embed.html' %}` trước `</body>`
3. Thêm CSS và Script vào `<head>` của base template

---

## Bước 3: Tùy chỉnh giao diện (CSS Variables)

| CSS Variable | Mô tả | Ví dụ |
|---|---|---|
| `--df-messenger-font-color` | Màu chữ | `#000` |
| `--df-messenger-font-family` | Font chữ | `Google Sans` |
| `--df-messenger-chat-background` | Nền chat window | `#f3f6fc` |
| `--df-messenger-message-user-background` | Nền tin nhắn user | `#d3e3fd` |
| `--df-messenger-message-bot-background` | Nền tin nhắn bot | `#fff` |
| `--df-messenger-button-titlebar-color` | Màu thanh tiêu đề | `#10b981` |

Tham khảo đầy đủ: [CSS Customizations](https://cloud.google.com/dialogflow/cx/docs/concept/integration/dialogflow-messenger/css)

---

## Bước 4: Deploy

### Nếu dùng Ubuntu Server + Git (như dự án này)

```bash
# Trên máy local (Windows)
git add .
git commit -m "feat: integrate Vertex AI chatbot widget"
git push origin main

# SSH vào server
ssh user@server_ip
cd /var/www/YourProject && git pull origin main
sudo systemctl restart your_service
```

### Nếu dùng hosting tĩnh (Netlify, Vercel, GitHub Pages...)
Chỉ cần push code — tự động deploy.

### Nếu dùng WordPress
Dán đoạn embed code vào **Appearance → Theme Editor → footer.php** hoặc sử dụng plugin "Insert Headers and Footers".

---

## Tham khảo


- [Dialogflow CX Messenger - Tài liệu chính thức](https://cloud.google.com/dialogflow/cx/docs/concept/integration/dialogflow-messenger)
- [HTML Customizations](https://cloud.google.com/dialogflow/cx/docs/concept/integration/dialogflow-messenger/html)
- [CSS Customizations](https://cloud.google.com/dialogflow/cx/docs/concept/integration/dialogflow-messenger/css)
- [JavaScript Events](https://cloud.google.com/dialogflow/cx/docs/concept/integration/dialogflow-messenger/javascript-events)
- [JavaScript Functions](https://cloud.google.com/dialogflow/cx/docs/concept/integration/dialogflow-messenger/javascript-functions)
