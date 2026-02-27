# Hướng dẫn Triển khai ESG Scorer lên máy chủ (VPS)

Tài liệu này hướng dẫn chi tiết các bước để đưa dự án **ESG Scorer** từ mã nguồn trên GitHub lên chạy thực tế trên một máy chủ ảo (VPS) chạy hệ điều hành Linux (khuyên dùng Ubuntu 20.04 hoặc 22.04 LTS).

---

## Bước 1: Chuẩn bị máy chủ (Prerequisites)

Sau khi thuê VPS (từ DigitalOcean, Vultr, AWS, hoặc nhà cung cấp VN), hãy kết nối SSH vào VPS của bạn:

```bash
ssh root@<IP_CUB_VPS>
```

Tiến hành cập nhật hệ thống và cài đặt các công cụ cơ bản (**Python 3.11+**, **Git**, **Nginx**):

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git nginx -y
```

---

## Bước 2: Tải mã nguồn về VPS (Clone Repository)

Di chuyển đến thư mục `/var/www/` (nơi khuyên dùng để chứa web app) và tải code của bạn từ GitHub về:

```bash
cd /var/www/
sudo git clone https://github.com/hoang-bd23/Esg_scorer.git
cd Esg_scorer
```

*(Nếu repo của bạn để chế độ Private, Git sẽ yêu cầu nhập Username và Personal Access Token).*

---

## Bước 3: Thiết lập môi trường ảo và Cài đặt thư viện

Khởi tạo một môi trường ảo (Virtual Environment) để cài đặt thư viện cho dự án mà không làm ảnh hưởng đến hệ thống chung của VPS:

```bash
# Tạo môi trường ảo tên là venv
python3 -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate
```

Sau khi kích hoạt, dấu nhắc lệnh của bạn sẽ có tiền tố `(venv)`. Tiếp tục cài đặt các thư viện:

```bash
pip install --upgrade pip
pip install -e .
```

*Lưu ý: Dự án sử dụng `pyproject.toml` để quản lý thư viện (thay cho file `requirements.txt` kiểu cũ). Khi chạy lệnh `pip install -e .`, toàn bộ thư viện cần thiết sẽ tự động được tải và cài đặt.*

---

## Bước 4: Chạy thử ứng dụng (Test Run)

Trước khi cấu hình chạy nền, ta nên chạy thử xem app có lỗi gì không:

```bash
uvicorn esg_scorer.main:app --host 127.0.0.1 --port 8000
```
Nếu bạn thấy dòng chữ `Application startup complete.`, chúc mừng bạn ứng dụng đã sẵn sàng! Bấm `Ctrl+C` để dừng.

---

## Bước 5: Cấu hình hệ thống để ứng dụng chạy ngầm (Systemd Service)

Để ứng dụng tự động chạy lại nếuVPS bị khởi động lại (restart) hoặc khi bị sập (crash), bạn cần tạo một `systemd service`.

Tạo file cấu hình:
```bash
sudo nano /etc/systemd/system/esg_scorer.service
```

Dán nội dung sau vào (Chú ý thay đổi `User=_Tên_User_` nếu bạn không dùng user root, và kiểm tra lại đường dẫn):

```ini
[Unit]
Description=Gunicorn instance to serve ESG Scorer Backend
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/Esg_scorer
Environment="PATH=/var/www/Esg_scorer/venv/bin"
ExecStart=/var/www/Esg_scorer/venv/bin/uvicorn esg_scorer.main:app --host 127.0.0.1 --port 8000

[Install]
WantedBy=multi-user.target
```
*(Ấn `Ctrl+O` -> `Enter` để lưu, sau đó `Ctrl+X` để thoát nano).*

Sau đó, tiến hành kích hoạt và chạy service:

```bash
sudo systemctl daemon-reload
sudo systemctl start esg_scorer
sudo systemctl enable esg_scorer
```

Kiểm tra trạng thái (nếu thấy chữ `active (running)` màu xanh là OK):
```bash
sudo systemctl status esg_scorer
```

---

## Bước 6: Cấu hình Nginx (Reverse Proxy)

Nginx đóng vai trò là "người gác cổng", nhận request từ Port 80 (HTTP) bên ngoài internet và đẩy cho Uvicorn ở Port 8000 bên trong VPS.

Tạo file cấu hình Nginx mới:
```bash
sudo nano /etc/nginx/sites-available/esg_scorer
```

Dán nội dung sau vào (Thay `your_domain_or_IP` bằng IP của VPS hoặc tên miền của bạn nếu có):

```nginx
server {
    listen 80;
    server_name your_domain_or_IP; # Thay bằng IP VPS (VD: 103.1.2.3) hoặc domain (VD: esg.doanhnghiep.com)

    # Cho phép upload file lớn lên tới 500MB (Rất quan trọng cho file PDF tải lên)
    client_max_body_size 500M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Kích hoạt file cấu hình vừa tạo và **xóa trang mặc định của Nginx** (để tránh bị đụng độ trang "Welcome to nginx!"):
```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/esg_scorer /etc/nginx/sites-enabled/
```

Kiểm tra xem file cấu hình Nginx có lỗi cú pháp không:
```bash
sudo nginx -t
```
Nếu kết quả `Syntax is OK`, khởi động lại Nginx:
```bash
sudo systemctl restart nginx
```

---

## Hoàn tất! 🎉
Bây giờ, bạn có thể tự hào mở trình duyệt trên máy tính/điện thoại, gõ địa chỉ IP của VPS (hoặc tên miền) vào để truy cập trang web.

**Cách truy cập:**
1. Mở Chrome, Firefox, Safari...
2. Gõ địa chỉ IP VPS của bạn vào thanh địa chỉ.
   *Ví dụ: `http://103.111.222.333`* hoặc `http://esg.doanhnghiep.com`
3. Trang **Bảng Xếp Hạng ESG Scorer** của bạn sẽ ngay lập tức hiện ra mượt mà và thường trực trực tuyến 24/7! (Lần đầu truy cập có thể sẽ trống vì chưa có dữ liệu, hãy ấn sang tab Chấm Điểm Ngay để bắt đầu upload).

---

## (Phụ lục) Làm sao để cập nhật code mới trong tương lai?

Khi bạn sửa code trên máy tính => Xong ấn commit & push lên GitHub. Bạn làm gì để VPS tự cập nhật bản web mới nhất đó?

Bạn chỉ cần kết nối SSH vào VPS và chạy 3 dòng lệnh sau:

```bash
cd /var/www/Esg_scorer
git pull origin main
sudo systemctl restart esg_scorer
```
Hệ thống sẽ kéo bản code mới nhất từ GitHub về thư mục VPS và khởi động lại trang web chỉ chớp mắt. Chúc bạn thành công!
