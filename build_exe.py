# -*- coding: utf-8 -*-
"""
Build script để đóng gói ESG Scorer thành file .exe bằng PyInstaller.

Cách sử dụng:
    python build_exe.py

Sau khi chạy xong, thư mục `dist/ChamDiemESG/` sẽ chứa phần mềm hoàn chỉnh.
Gửi toàn bộ thư mục đó (nén thành .zip) cho người dùng.
"""
import subprocess
import sys
import os
import shutil

def install_pyinstaller():
    """Cài PyInstaller nếu chưa có."""
    try:
        import PyInstaller
        print("[OK] PyInstaller da duoc cai dat.")
    except ImportError:
        print("[...] Dang cai dat PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] Da cai xong PyInstaller.")

def build():
    install_pyinstaller()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    # Đường dẫn tới thư mục templates và static
    templates_src = os.path.join(base_dir, "src", "esg_scorer", "web", "templates")
    scoring_dir = os.path.join(base_dir, "scoring principles")
    
    # Lệnh PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "ChamDiemESG",
        "--noconfirm",
        "--console",  # Giữ cửa sổ Console để người dùng thấy trạng thái
        "--icon", "NONE",
        # Thêm các thư mục dữ liệu cần thiết
        "--add-data", f"{templates_src};src/esg_scorer/web/templates",
        "--add-data", f"{scoring_dir};scoring principles",
        # Các hidden imports mà PyInstaller có thể bỏ sót
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.loops",
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.protocols",
        "--hidden-import", "uvicorn.protocols.http",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.websockets",
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "uvicorn.lifespan",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "uvicorn.lifespan.off",
        "--hidden-import", "esg_scorer",
        "--hidden-import", "esg_scorer.main",
        "--hidden-import", "esg_scorer.api",
        "--hidden-import", "esg_scorer.api.routes",
        "--hidden-import", "esg_scorer.api.batch_routes",
        "--hidden-import", "esg_scorer.core",
        "--hidden-import", "esg_scorer.core.pdf_extractor",
        "--hidden-import", "esg_scorer.core.scoring_engine",
        "--hidden-import", "esg_scorer.core.keywords",
        "--hidden-import", "esg_scorer.core.framework",
        "--hidden-import", "esg_scorer.models",
        "--hidden-import", "esg_scorer.models.schemas",
        "--hidden-import", "esg_scorer.models.database",
        "--hidden-import", "esg_scorer.services",
        "--hidden-import", "esg_scorer.services.export_service",
        "--hidden-import", "esg_scorer.services.batch_service",
        "--hidden-import", "pdfplumber",
        "--hidden-import", "pdfminer",
        "--hidden-import", "pdfminer.high_level",
        "--hidden-import", "openpyxl",
        "--hidden-import", "sqlalchemy",
        "--hidden-import", "sqlalchemy.dialects.sqlite",
        "--hidden-import", "aiosqlite",
        "--hidden-import", "multipart",
        "--hidden-import", "python_multipart",
        # Collect tất cả submodules của các package phức tạp
        "--collect-submodules", "uvicorn",
        "--collect-submodules", "pdfplumber",
        "--collect-submodules", "pdfminer",
        "--collect-submodules", "sqlalchemy",
        # File chính
        "launcher.py"
    ]
    
    print("\n" + "=" * 50)
    print("  BAT DAU DONG GOI .EXE")
    print("=" * 50)
    print("Dang chay PyInstaller, qua trinh nay mat 2-5 phut...\n")
    
    subprocess.check_call(cmd)
    
    # Copy thư mục src vào dist để uvicorn.run tìm được module
    dist_dir = os.path.join(base_dir, "dist", "ChamDiemESG")
    src_dest = os.path.join(dist_dir, "src")
    if os.path.exists(src_dest):
        shutil.rmtree(src_dest)
    shutil.copytree(
        os.path.join(base_dir, "src"),
        src_dest,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
    )
    
    # Tạo thư mục data cần thiết
    os.makedirs(os.path.join(dist_dir, "data", "cache"), exist_ok=True)
    os.makedirs(os.path.join(dist_dir, "batch_uploads"), exist_ok=True)
    os.makedirs(os.path.join(dist_dir, "exports"), exist_ok=True)
    
    print("\n" + "=" * 50)
    print("  DONG GOI THANH CONG!")
    print("=" * 50)
    print(f"  Thu muc phan mem:  dist/ChamDiemESG/")
    print(f"  File chay chinh:   dist/ChamDiemESG/ChamDiemESG.exe")
    print()
    print("  HUONG DAN GUI CHO NGUOI DUNG:")
    print("  1. Nen thu muc 'dist/ChamDiemESG' thanh file .zip")
    print("  2. Gui file .zip cho nguoi can dung")
    print("  3. Ho chi can giai nen va nhan dup 'ChamDiemESG.exe'")
    print("=" * 50)

if __name__ == "__main__":
    build()
