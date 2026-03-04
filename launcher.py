# -*- coding: utf-8 -*-
"""
ESG Scorer Launcher - Điểm vào chính cho phần mềm đóng gói (.exe)
Khởi động server FastAPI + Tự động mở trình duyệt Web.
"""
import sys
import os
import socket
import webbrowser
import threading
import time

def get_base_dir():
    """Lấy đường dẫn gốc, hỗ trợ cả chạy bình thường và chạy từ .exe (PyInstaller)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def find_free_port(preferred: int = 8686) -> int:
    """Tìm cổng trống. Ưu tiên cổng preferred, nếu bận thì để OS tự chọn."""
    # Thử cổng ưu tiên trước
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", preferred))
            s.close()
            return preferred
        except OSError:
            pass
    
    # Nếu cổng ưu tiên bận, để OS tự cấp cổng trống
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        return port

def open_browser(port: int):
    """Đợi 2.5 giây cho server sẵn sàng rồi mở trình duyệt."""
    time.sleep(2.5)
    webbrowser.open(f"http://127.0.0.1:{port}")

def main():
    base_dir = get_base_dir()
    os.chdir(base_dir)
    
    # Thêm thư mục src vào PYTHONPATH
    src_dir = os.path.join(base_dir, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    # Tạo thư mục cần thiết nếu chưa có
    os.makedirs("data/cache", exist_ok=True)
    os.makedirs("batch_uploads", exist_ok=True)
    os.makedirs("exports", exist_ok=True)
    
    # Tìm cổng trống
    port = find_free_port(8686)
    
    if port != 8686:
        print(f"  [!] Cong 8686 dang ban, tu dong chuyen sang cong {port}")
    
    print("=" * 50)
    print("  HE THONG CHAM DIEM ESG - KLD Framework")
    print("=" * 50)
    print(f"  Dang khoi dong tai: http://127.0.0.1:{port}")
    print("  Trinh duyet se tu dong mo sau vai giay...")
    print("  De tat phan mem: Dong cua so nay hoac nhan Ctrl+C")
    print("=" * 50)
    
    # Mở trình duyệt trong thread riêng
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    # Khởi động Uvicorn server
    import uvicorn
    config = uvicorn.Config(
        "esg_scorer.main:app",
        host="127.0.0.1",
        port=port,
        log_level="warning",
        reload=False
    )
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    main()
