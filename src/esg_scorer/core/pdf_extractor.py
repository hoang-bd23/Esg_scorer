import os
import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any
import pdfplumber

# Thư mục gốc project (lên 3 cấp từ core/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

class PDFExtractor:
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            cache_dir = str(_PROJECT_ROOT / "data" / "cache")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, pdf_path: str) -> Path:
        """Tạo đường dẫn file cache dựa trên mã băm của tên file"""
        # Sử dụng hash của đường dẫn tuyệt đối để tránh trùng lặp tên
        abs_path = os.path.abspath(pdf_path)
        file_hash = hashlib.md5(abs_path.encode()).hexdigest()
        filename = Path(pdf_path).name
        return self.cache_dir / f"{filename}_{file_hash}.jsonl"
        
    def _read_from_cache(self, cache_path: Path) -> Optional[List[Dict[str, Any]]]:
        if cache_path.exists():
            pages = []
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            pages.append(json.loads(line))
                return pages
            except Exception:
                return None
        return None

    def _save_to_cache(self, cache_path: Path, pages: List[Dict[str, Any]]):
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                for page in pages:
                    f.write(json.dumps(page, ensure_ascii=False) + '\n')
        except Exception:
            pass

    def extract_text(self, pdf_path: str, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Trích xuất văn bản từ file PDF. 
        Trả về danh sách các trang, mỗi trang là một dict: {"page_num": int, "text": str}.
        Nếu use_cache=True, sẽ thử đọc từ file .jsonl đã lưu trước đó.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Không tìm thấy file PDF tại: {pdf_path}")
            
        cache_path = self._get_cache_path(pdf_path)
        
        if use_cache:
            cached_pages = self._read_from_cache(cache_path)
            if cached_pages:
                return cached_pages
                
        # Trích xuất nếu không có cache
        extracted_pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Sử dụng hàm extract_text hỗ trợ tốt tiếng Việt
                text = page.extract_text(x_tolerance=2, y_tolerance=3)
                if text:
                    extracted_pages.append({
                        "page_num": page.page_number,
                        "text": text.strip()
                    })
                    
        if use_cache and extracted_pages:
            self._save_to_cache(cache_path, extracted_pages)
            
        return extracted_pages
