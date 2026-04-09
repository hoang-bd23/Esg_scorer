# 🚀 Hướng Dẫn Cấu Hình Google Cloud Storage Trên Ubuntu Server

Mã nguồn (code) tính năng tự động upload PDF lên GCS Bucket đã được mình hoàn thiện và push lên kho lưu trữ chính. 
Tuy nhiên, để Code chạy thành công, Server Ubuntu của bạn cần **2 thứ quan trọng**: (1) Thư viện Python mới và (2) Chìa khóa xác thực `json` mà bạn vừa cung cấp.

Bạn hãy thao tác theo từng bước sau ngay trên cửa sổ dòng lệnh (Terminal) kết nối với Ubuntu Server:

---

### Bước 1: Kéo Code mới và Cài đặt Thư Viện
Đăng nhập SSH vào server Ubuntu (`ssh bdhzxc23@192.168.1.124` như bạn hay làm), rồi chạy lần lượt:

```bash
cd /var/www/Esg_scorer
git pull origin main

# Bật môi trường ảo và cài thư viện mình mới thêm (google-cloud-storage)
source venv/bin/activate
pip install -e .
deactivate
```

---

### Bước 2: Tải Key xác thực lên Server

Hiện tại file json đang nằm trên laptop Windows của bạn. Chúng ta cần chuyển nó sang Server Ubuntu (ví dụ cất vào `/var/www/Esg_scorer/key.json`). Bạn có thể dùng cách tạo nhanh file trên server:

Trên server Ubuntu, chạy:
```bash
nano /var/www/Esg_scorer/key.json
```
Sau đó, hãy **mở file JSON trên VS Code Windows**, **Copy toàn bộ nội dung** và **Paste** thẳng vào màn hình `nano` trên Server. 
Xong nhấn `Ctrl + O` -> `Enter` để lưu -> `Ctrl + X` để thoát.

Phân quyền bảo mật để chỉ hệ thống được phép đọc:
```bash
sudo chown bdhzxc23:www-data /var/www/Esg_scorer/key.json
sudo chmod 640 /var/www/Esg_scorer/key.json
```

---

### Bước 3: Gắn Biến Môi Trường vào Dịch Vụ SystemD

Mã nguồn Python cần biết chỗ lấy "chìa khoá" để kết nối với Google. Ta cần báo cho hệ thống dịch vụ chạy ngầm biết.

Chạy lệnh sửa file cấu hình dịch vụ:
```bash
sudo nano /etc/systemd/system/esg_scorer.service
```

Tìm đến cục `[Service]` và thêm dòng `Environment=` này vào (nghiêm ngặt viết dưới dòng `WorkingDirectory`):

```ini
[Service]
User=bdhzxc23
Group=www-data
WorkingDirectory=/var/www/Esg_scorer
Environment="PATH=/var/www/Esg_scorer/venv/bin"
Environment="GOOGLE_APPLICATION_CREDENTIALS=/var/www/Esg_scorer/key.json"
Environment="GCP_BUCKET_NAME=rag_bucket_us-central1"
#... các phần còn lại giữ nguyên
```
Lưu lại bằng `Ctrl + O` -> `Enter` -> `Ctrl + X`.

---

### Bước 4: Khởi Động Lại Hệ Thống là Hoàn Tất

Cập nhật lại cho SystemD biết bạn vừa sửa file và khởi động lại API:

```bash
sudo systemctl daemon-reload
sudo systemctl restart esg_scorer
```

**✅ Xong!** Kể từ bây giờ, bất cứ khi nào có ai up 1 file PDF lên Tool chấm điểm, nó sẽ ngay lập tức được chép ngược vào thư mục `documents/tên_file.pdf` trong GCP Bucket `rag_bucket_us-central1` của bạn!
