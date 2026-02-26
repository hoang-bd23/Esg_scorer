import os
from pathlib import Path
from typing import List, Optional
import concurrent.futures
from tqdm import tqdm

from ..core.pdf_extractor import PDFExtractor
from ..core.scoring_engine import RuleBasedScoringEngine
from ..core.keywords import KLD_KEYWORDS
from ..models.schemas import CompanyESGResult, ESGScoreWeights

class BatchScoringService:
    def __init__(self, use_cache: bool = True):
        # Không khởi tạo extractor/engine ở __init__ nếu dùng multiprocessing
        # Vì nó có thể gây lỗi pickle khi fork/spawn process.
        self.use_cache = use_cache

    @staticmethod
    def _process_single_file(pdf_path: str, weights: ESGScoreWeights, use_cache: bool) -> Optional[CompanyESGResult]:
        try:
            # Khởi tạo instance mỗi process
            extractor = PDFExtractor()
            engine = RuleBasedScoringEngine(KLD_KEYWORDS)
            
            filename = Path(pdf_path).name
            company_name = filename.replace(".pdf", "")
            
            text = extractor.extract_text(pdf_path, use_cache=use_cache)
            if not text:
                return None
                
            result = engine.evaluate(company_name, 2024, text)
            result.weights = weights
            return result
        except Exception as e:
            # Dấu lỗi ở CLI console nếu muốn
            return None

    def process_folder(self, folder_path: str, weights: ESGScoreWeights, max_workers: int = 4) -> List[CompanyESGResult]:
        """Xử lý hàng loạt file PDF trong thư mục bằng đa luồng"""
        folder = Path(folder_path)
        if not folder.exists() or not folder.is_dir():
            raise NotADirectoryError(f"Không tìm thấy thư mục: {folder_path}")
            
        pdf_files = list(folder.glob("*.pdf"))
        if not pdf_files:
            return []
            
        results = []
        # Tối ưu cho 700-800 files bằng ProcessPoolExecutor
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Map kết quả
            futures = {executor.submit(self._process_single_file, str(path), weights, self.use_cache): path for path in pdf_files}
            
            # Progress bar với tqdm
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(pdf_files), desc="Đang phân tích ESG"):
                res = future.result()
                if res is not None:
                    results.append(res)
                    
        return results
