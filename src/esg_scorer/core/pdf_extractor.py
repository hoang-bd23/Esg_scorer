import os
import hashlib
from pathlib import Path
from typing import Optional
import pdfplumber

class PDFExtractor:
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, pdf_path: str) -> Path:
        """Tạo đường dẫn file cache dựa trên mã băm của tên file"""
        # Sử dụng hash của đường dẫn tuyệt đối để tránh trùng lặp tên
        abs_path = os.path.abspath(pdf_path)
        file_hash = hashlib.md5(abs_path.encode()).hexdigest()
        filename = Path(pdf_path).name
        return self.cache_dir / f"{filename}_{file_hash}.txt"
        
    def _read_from_cache(self, cache_path: Path) -> Optional[str]:
        if cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def _save_to_cache(self, cache_path: Path, text: str):
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(text)

    def extract_text(self, pdf_path: str, use_cache: bool = True) -> str:
        """
        Trích xuất văn bản từ file PDF. 
        Nếu use_cache=True, sẽ thử đọc từ file .txt đã lưu trước đó.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Không tìm thấy file PDF tại: {pdf_path}")
            
        cache_path = self._get_cache_path(pdf_path)
        
        if use_cache:
            cached_text = self._read_from_cache(cache_path)
            if cached_text:
                return cached_text
                
        # Trích xuất nếu không có cache
        extracted_text = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                # Sử dụng hàm extract_text hỗ trợ tốt tiếng Việt
                text = page.extract_text(x_tolerance=2, y_tolerance=3)
                if text:
                    extracted_text.append(f"--- PAGE {i+1} ---\n{text}")
                    
        full_text = "\n\n".join(extracted_text)
        
        if use_cache:
            self._save_to_cache(cache_path, full_text)
            
        return full_text
