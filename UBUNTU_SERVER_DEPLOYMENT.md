# 🖥️ Hướng dẫn Triển khai ESG Scorer trên Laptop Ubuntu Server (Qua WiFi)

> **Mục tiêu:** Biến chiếc laptop cũ chạy Ubuntu Server (kết nối WiFi) thành một máy chủ web thực thụ, cho phép mọi người trong mạng LAN (hoặc từ Internet) truy cập ứng dụng **ESG Scorer** qua địa chỉ IP.

---

## Tổng quan Kiến trúc

```
Người dùng (trình duyệt)
        │
        ▼
  [ IP Công cộng : Port 80 ]  ← Router NAT/Port Forwarding
        │
        ▼
  [ Nginx - Reverse Proxy ]   ← Laptop Ubuntu Server (IP nội bộ)
        │
        ▼
  [ Uvicorn : Port 8000 ]     ← Ứng dụng FastAPI
        │
        ▼
  [ SQLite Database ]          ← Lưu trữ dữ liệu
```

---

## Phần A: Chuẩn bị Laptop Ubuntu Server

### Bước 1: Cài đặt Ubuntu Server (nếu chưa có)

Nếu laptop đã chạy Ubuntu Server rồi, bỏ qua bước này.

1. Tải **Ubuntu Server 22.04 LTS** từ: https://ubuntu.com/download/server
2. Tạo USB boot bằng **Rufus** (Windows) hoặc **Balena Etcher**
3. Boot laptop từ USB → Cài đặt Ubuntu Server
4. Trong quá trình cài đặt:
   - ✅ Chọn **Install OpenSSH server** (rất quan trọng để điều khiển từ xa)
   - ✅ Ở bước **Network connections**: chọn mạng WiFi và nhập mật khẩu
   - Đặt username và password

### Bước 2: Xác định tên card WiFi và IP nội bộ

Sau khi cài xong, đăng nhập trực tiếp trên laptop và chạy:

```bash
# Xem tên card WiFi (thường là wlp2s0, wlp3s0, wlan0...)
ip link show | grep -i wl

# Xem IP hiện tại
ip addr show
```

Tìm dòng có `inet 192.168.x.x` dưới card WiFi — đó là **IP nội bộ** của laptop.
Ví dụ: card WiFi là `wlp2s0`, IP là `192.168.1.100`

> [!TIP]
> Ghi nhớ **tên card WiFi** và **IP** này, bạn sẽ dùng ở tất cả các bước tiếp theo.

### Bước 3: Kết nối SSH từ máy tính chính (Windows)

Từ giờ trở đi, bạn có thể điều khiển laptop Ubuntu từ xa bằng SSH, không cần ngồi trước nó nữa.

Mở **PowerShell** hoặc **Terminal** trên máy Windows và chạy:

```powershell
ssh username@192.168.1.100
```
*(Thay `username` bằng tên user đã tạo khi cài Ubuntu, thay IP cho đúng)*

### Bước 4: Cài đặt WiFi tools & Cố định IP (Static IP) - Rất quan trọng!

Đầu tiên, cài đặt công cụ quản lý WiFi:

```bash
sudo apt update
sudo apt install wpasupplicant wireless-tools -y
```

Mặc định, router sẽ cấp IP động (DHCP) — nghĩa là mỗi lần laptop khởi động lại, IP có thể thay đổi. Ta cần **cố định IP** để tránh bị mất kết nối.

Tìm IP Gateway (router) trước:

```bash
ip route | grep default
# Kết quả VD: default via 192.168.1.1 dev wlp2s0
```

Bây giờ chỉnh file cấu hình mạng:

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

**Xóa toàn bộ** nội dung cũ và dán nội dung sau (thay đổi cho phù hợp với mạng của bạn):

```yaml
network:
  version: 2
  renderer: networkd            # ← BẮT BUỘC dùng NetworkManager cho WiFi
  wifis:
    wlp2s0:                            # ← Thay bằng tên card WiFi thực tế (Bước 2)
      dhcp4: no
      addresses:
        - 192.168.1.124/24             # ← IP bạn muốn cố định
      routes:
        - to: default
          via: 192.168.1.1             # ← IP Router/Gateway (vừa tìm ở trên)
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]  # DNS Google + Cloudflare
      access-points:
        "TEN_WIFI_NHA_BAN":            # ← Thay bằng tên WiFi (phân biệt HOA/thường)
          password: "MAT_KHAU_WIFI"    # ← Thay bằng mật khẩu WiFi
```

> [!IMPORTANT]
> **Lưu ý quan trọng:**
> - Tên WiFi phải **chính xác** y chang bao gồm HOA/thường, dấu cách. Xem bằng: `nmcli dev wifi list` hoặc `iwlist wlp2s0 scan | grep ESSID`
> - Chọn IP cố định **ngoài vùng DHCP** của router để tránh xung đột (VD: router cấp DHCP từ .2 đến .99, thì ta chọn .100 trở lên)
> - Nếu không biết tên card WiFi: chạy `ip link show | grep -i wl` (Bước 2)

Áp dụng cấu hình:

```bash
sudo netplan generate   # Kiểm tra cú pháp YAML
sudo netplan apply      # Áp dụng
```

Chờ 5-10 giây, kiểm tra lại kết nối:

```bash
ping -c 3 google.com    # Phải thấy "3 packets transmitted, 3 received"
ip addr show wlo1     # Phải thấy IP 192.168.1.124
```

> [!WARNING]
> Nếu mất kết nối WiFi sau `netplan apply`, bạn phải ngồi trước laptop để sửa. Kiểm tra kỹ tên WiFi, mật khẩu và tên card mạng trước khi áp dụng!

---

## Phần B: Cài đặt Ứng dụng ESG Scorer

### Bước 5: Cập nhật hệ thống và cài đặt công cụ

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git nginx ufw network-manager -y
```

> [!NOTE]
> `network-manager` giúp quản lý WiFi thuận tiện hơn (xem mạng, chuyển WiFi, kiểm tra tín hiệu).

### Bước 6: Tải mã nguồn

```bash
cd /var/www/
sudo git clone https://github.com/hoang-bd23/Esg_scorer.git
cd Esg_scorer
```

*(Nếu repo Private → Git sẽ hỏi Username + Personal Access Token của GitHub)*

### Bước 7: Tạo môi trường ảo & Cài thư viện

```bash
sudo chown -R bdhzxc23:bdhzxc23 /var/www/Esg_scorer
cd /var/www/Esg_scorer
python3 -m venv venv

source venv/bin/activate
pip install --upgrade pip
pip install -e .
```

### Bước 8: Chạy thử

```bash
uvicorn esg_scorer.main:app --host 0.0.0.0 --port 8000
```

Mở trình duyệt trên máy Windows, gõ `http://192.168.1.124:8000` — nếu thấy trang web hiện lên là thành công! Nhấn `Ctrl+C` trên SSH để dừng.

> [!NOTE]
> Khác với VPS guide cũ dùng `--host 127.0.0.1`, ở đây ta dùng `--host 0.0.0.0` để cho phép truy cập từ các máy khác trong mạng. Nginx sẽ đảm nhiệm bảo mật ở bước sau.

---

## Phần C: Cấu hình chạy ngầm & Reverse Proxy

### Bước 9: Tạo Systemd Service (Chạy ngầm 24/7)

```bash
sudo nano /etc/systemd/system/esg_scorer.service
```

Dán nội dung sau:

```ini
[Unit]
Description=ESG Scorer FastAPI Application
# Dùng network-online.target thay vì network.target để đảm bảo WiFi đã kết nối xong
After=network-online.target
Wants=network-online.target

[Service]
# Thay "your_username" bằng user thật (chạy: whoami)
User=your_username
Group=www-data
WorkingDirectory=/var/www/Esg_scorer
Environment="PATH=/var/www/Esg_scorer/venv/bin"
ExecStart=/var/www/Esg_scorer/venv/bin/uvicorn esg_scorer.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5
# Đợi thêm 10s sau khi khởi động để WiFi ổn định
ExecStartPre=/bin/sleep 10

[Install]
WantedBy=multi-user.target
```

Kích hoạt và chạy:

```bash
sudo systemctl daemon-reload
sudo systemctl start esg_scorer
sudo systemctl enable esg_scorer    # Tự khởi động khi bật laptop
```

Kiểm tra trạng thái (phải thấy `active (running)` màu xanh):

```bash
sudo systemctl status esg_scorer
```

### Bước 10: Cấu hình Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/esg_scorer
```

Dán nội dung:

```nginx
server {
    listen 80;
    server_name _;   # Chấp nhận mọi request (vì ta dùng IP, không có domain)

    client_max_body_size 500M;   # Cho phép upload file PDF lớn

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout dài hơn cho việc xử lý PDF lớn
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
```

Kích hoạt cấu hình:

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/esg_scorer /etc/nginx/sites-enabled/
sudo nginx -t                    # Kiểm tra cú pháp → phải thấy "Syntax is OK"
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### Bước 11: Mở Firewall

```bash
sudo ufw allow 22/tcp       # SSH (QUAN TRỌNG: mở cái này trước!)
sudo ufw allow 80/tcp       # HTTP
sudo ufw allow 443/tcp      # HTTPS (dùng sau nếu cần)
sudo ufw enable             # Bật firewall
sudo ufw status             # Kiểm tra
```

> [!CAUTION]
> **Phải mở port 22 TRƯỚC khi `ufw enable`!** Nếu không, bạn sẽ bị khóa ngoài SSH. Khi đó phải ra ngồi trước laptop để sửa.

---

## Phần D: Mở truy cập từ Internet (Cloudflare Tunnel)

> Phần này cho phép người **bên ngoài mạng nhà** truy cập được. Nếu chỉ cần dùng trong mạng LAN nội bộ, bạn có thể bỏ qua.
>
> Dùng **Cloudflare Tunnel** — không cần mở port, không cần quyền truy cập router, được **HTTPS miễn phí**!

```
Người dùng → https://esg.buiduchoang.dev
                     │
                     ▼
           [ Cloudflare Edge ]     ← Bảo mật, HTTPS, CDN
                     │
               (Tunnel mã hóa)    ← Laptop tự kết nối ra, KHÔNG cần mở port
                     │
                     ▼
           [ Laptop Ubuntu ]      ← http://127.0.0.1:8000
```

### Bước 12: Đăng ký Cloudflare (Miễn phí)

1. Truy cập https://dash.cloudflare.com/sign-up → Tạo tài khoản miễn phí
2. Bạn cần có **1 tên miền** (domain). Nếu chưa có:
   - Mua domain giá rẻ (~30k/năm) tại Namecheap, Tên Miền Việt Nam, hoặc mua luôn trên Cloudflare
   - Hoặc dùng miễn phí qua **`trycloudflare`** (xem Bước 12b bên dưới — không cần domain)
3. Thêm domain vào Cloudflare → Đổi Nameserver theo hướng dẫn của Cloudflare

### Bước 12b: Chạy nhanh KHÔNG cần domain (Try Cloudflare)

Nếu chỉ muốn test nhanh mà chưa có domain:

```bash
# Cài cloudflared
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o /tmp/cloudflared.deb
sudo dpkg -i /tmp/cloudflared.deb

# Chạy tunnel tạm thời (sẽ được 1 URL ngẫu nhiên)
cloudflared tunnel --url http://127.0.0.1:8000
```

Kết quả sẽ in ra 1 URL dạng:
```
https://random-words-here.trycloudflare.com
```

Gửi link này cho bất kỳ ai → họ truy cập được ngay! Nhưng **URL sẽ thay đổi mỗi lần chạy lại**, nên chỉ phù hợp để test. Để có URL cố định, làm tiếp các bước dưới.

### Bước 13: Cài đặt Cloudflare Tunnel (URL cố định)

**13.1. Cài đặt `cloudflared` trên laptop Ubuntu:**

```bash
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o /tmp/cloudflared.deb
sudo dpkg -i /tmp/cloudflared.deb
```

**13.2. Đăng nhập Cloudflare:**

```bash
cloudflared tunnel login
```

Lệnh này sẽ in ra 1 URL → Mở URL đó trên trình duyệt → Chọn domain của bạn → Authorize.

**13.3. Tạo Tunnel:**

```bash
# Tạo tunnel tên "esg-scorer"
cloudflared tunnel create esg-scorer
```

Lệnh sẽ trả về **Tunnel ID** (dạng `a1b2c3d4-...`). Ghi nhớ ID này.

**13.4. Tạo file cấu hình:**

```bash
nano ~/.cloudflared/config.yml
```

Dán nội dung (thay thế cho đúng):

```yaml
tunnel: 7efa86cb-56da-4db5-a05f-8a61a991be59   # ← Thay bằng Tunnel ID ở bước 13.3
credentials-file: /home/bdhzxc23/.cloudflared/7efa86cb-56da-4db5-a05f-8a61a991be59.json

ingress:
  - hostname: buiduchoang.dev   # ← Thay bằng subdomain bạn muốn
    service: http://127.0.0.1:8000
  - service: http_status:404
```

**13.5. Tạo DNS record:**

```bash
cloudflared tunnel route dns esg-scorer buiduchoang.dev
```

*(Thay `esg.your-domain.com` bằng subdomain thật của bạn)*

### Bước 14: Chạy Tunnel như Service (Tự khởi động)

```bash
sudo cloudflared service install
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

Kiểm tra trạng thái:

```bash
sudo systemctl status cloudflared
```

### 🎉 Hoàn tất!

Bây giờ mọi người truy cập qua:
```
https://esg.buiduchoang.dev
```

> [!TIP]
> **Ưu điểm của Cloudflare Tunnel so với Port Forwarding:**
> - ✅ **Không cần quyền truy cập router** — hoạt động sau bất kỳ NAT/firewall nào
> - ✅ **HTTPS miễn phí** — Cloudflare tự cấp SSL certificate
> - ✅ **Không lộ IP nhà** — người dùng chỉ thấy IP của Cloudflare
> - ✅ **Chống DDoS miễn phí** — Cloudflare tự động bảo vệ
> - ✅ **IP động không thành vấn đề** — tunnel tự kết nối lại khi IP đổi

---

## Phần E: Bảo trì & Khắc phục sự cố

### Cập nhật code mới

```bash
cd /var/www/Esg_scorer
git pull origin main
sudo systemctl restart esg_scorer
```

### Xem log khi có lỗi

```bash
# Log ứng dụng
sudo journalctl -u esg_scorer -f --no-pager -n 50

# Log Nginx
sudo tail -f /var/log/nginx/error.log

# Log WiFi (khi mất kết nối)
sudo journalctl -u systemd-networkd -f --no-pager -n 30
```

### Ngăn laptop tắt màn hình / ngủ (Sleep)

Laptop cũ hay tự ngủ khi gập nắp. Cần tắt tính năng này:

```bash
sudo nano /etc/systemd/logind.conf
```

Tìm và sửa (hoặc thêm) các dòng sau:

```ini
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
IdleAction=ignore
```

Khởi động lại dịch vụ:

```bash
sudo systemctl restart systemd-logind
```

> [!TIP]
> Sau bước này, bạn có thể **gập nắp laptop** mà nó vẫn chạy bình thường!

### Tắt WiFi Power Management (Chống mất kết nối)

Ubuntu hay tự tắt WiFi để tiết kiệm pin. Ta cần vô hiệu hóa:

```bash
sudo nano /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
```

Dán nội dung:

```ini
[connection]
wifi.powersave = 2
```

*(Giá trị 2 = tắt power saving hoàn toàn)*

Hoặc tắt ngay lập tức (không cần reboot):

```bash
sudo iwconfig wlp2s0 power off    # Thay wlp2s0 bằng tên card WiFi thực tế
```

### Tạo WiFi Watchdog (Tự động kết nối lại khi mất WiFi)

WiFi đôi khi bị ngắt do router restart hoặc tín hiệu yếu. Script này sẽ tự kiểm tra và kết nối lại:

```bash
sudo nano /usr/local/bin/wifi-watchdog.sh
```

Dán nội dung:

```bash
#!/bin/bash
# WiFi Watchdog - Kiểm tra kết nối và tự phục hồi
LOG="/var/log/wifi-watchdog.log"
INTERFACE="wlp2s0"  # ← Thay bằng tên card WiFi thực tế

if ! ping -c 2 -W 5 8.8.8.8 > /dev/null 2>&1; then
    echo "$(date): WiFi mat ket noi! Dang khoi dong lai..." >> $LOG
    sudo ip link set $INTERFACE down
    sleep 3
    sudo ip link set $INTERFACE up
    sleep 10
    sudo netplan apply
    sleep 15
    if ping -c 2 -W 5 8.8.8.8 > /dev/null 2>&1; then
        echo "$(date): Da khoi phuc WiFi thanh cong!" >> $LOG
    else
        echo "$(date): THAT BAI - Khong the khoi phuc WiFi" >> $LOG
    fi
fi
```

```bash
sudo chmod +x /usr/local/bin/wifi-watchdog.sh
```

Thêm cron job chạy mỗi 2 phút:

```bash
sudo crontab -e
```

Thêm dòng này vào cuối:

```
*/2 * * * * /usr/local/bin/wifi-watchdog.sh
```

> [!TIP]
> Xem log watchdog: `sudo tail -f /var/log/wifi-watchdog.log`

### Kiểm tra WiFi & ứng dụng

```bash
# Kiểm tra WiFi đang kết nối
iwconfig wlp2s0

# Xem tín hiệu WiFi (số càng gần 0 càng mạnh, VD: -40 tốt, -80 yếu)
iwconfig wlp2s0 | grep -i signal

# Kiểm tra ứng dụng web
curl -s -o /dev/null -w "%{http_code}" http://localhost
# Kết quả: 200 = OK

# Xem trạng thái services
sudo systemctl status esg_scorer nginx
```

### Khởi động lại toàn bộ

```bash
sudo systemctl restart esg_scorer nginx
```

---

## Phụ lục A: So sánh Laptop Server vs VPS

| Tiêu chí | 🖥️ Laptop Server | ☁️ VPS |
|----------|:-:|:-:|
| Chi phí hàng tháng | **0đ** (chỉ tốn điện) | 100k - 500k/tháng |
| Tốc độ mạng | Phụ thuộc nhà mạng | Ổn định, nhanh |
| Uptime (hoạt động liên tục) | Phụ thuộc điện + internet nhà | 99.9% |
| IP tĩnh | ❌ Cần Dynamic DNS | ✅ Có sẵn |
| Bảo mật | Tự quản lý | Nhà cung cấp hỗ trợ |
| Phù hợp cho | Demo, dự án nhỏ, nội bộ | Production, doanh nghiệp |

## Phụ lục B: Cấu hình Ethernet (Cáp LAN) với Netplan

Nếu sau này bạn có thể cắm cáp mạng LAN trực tiếp, hãy đổi Netplan sang cấu hình này (ổn định hơn WiFi rất nhiều):

```yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    enp3s0:     # Thay bằng tên card LAN thực tế (xem: ip link show)
      dhcp4: no
      addresses:
        - 192.168.1.100/24
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

> [!TIP]
> Cáp LAN cho tốc độ ổn định hơn, không bị mất kết nối do tín hiệu yếu. Nếu có thể, hãy đặt laptop gần router và cắm cáp trực tiếp.

## Phụ lục C: Checklist nhanh

- [ ] Ubuntu Server đã cài đặt trên laptop
- [ ] WiFi kết nối OK (`ping google.com`)
- [ ] SSH hoạt động (`ssh user@ip`)
- [ ] IP nội bộ đã cố định (Static IP qua Netplan)
- [ ] WiFi Power Management đã tắt
- [ ] WiFi Watchdog đã cài (cron mỗi 2 phút)
- [ ] Gập nắp laptop không bị ngủ
- [ ] Clone code về `/var/www/Esg_scorer`
- [ ] Virtual env + thư viện đã cài
- [ ] `esg_scorer.service` đang chạy (`active (running)`)
- [ ] Nginx đã cấu hình và chạy
- [ ] Firewall (UFW) đã mở port 22, 80
- [ ] Port Forwarding trên router (nếu cần truy cập từ ngoài)
- [ ] Dynamic DNS đã cấu hình (nếu cần truy cập từ ngoài)
