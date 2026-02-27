from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional
import tempfile
import os
from pathlib import Path

from ..core.pdf_extractor import PDFExtractor
from ..core.scoring_engine import RuleBasedScoringEngine
from ..core.keywords import KLD_KEYWORDS
from ..models.schemas import CompanyESGResult
from fastapi import APIRouter
router = APIRouter(tags=["Scoring"])

# Note: Trong production thực tế nên dùng Dependency Injection
extractor = PDFExtractor()
engine = RuleBasedScoringEngine(KLD_KEYWORDS)


@router.post("/score", response_model=CompanyESGResult)
async def score_company(
    file: UploadFile = File(..., description="File PDF báo cáo của doanh nghiệp"),
    company_name: str = Form(..., description="Tên doanh nghiệp"),
    year: int = Form(2024, description="Năm báo cáo")
):
    """
    Tải lên một file PDF và thực hiện chấm điểm ESG tự động.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file PDF")
        
    try:
        # Lưu file tạm thời để extract
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
            
        # Xử lý PDF
        text = extractor.extract_text(temp_path, use_cache=False) # API thường upload trực tiếp
        if not text:
            raise HTTPException(status_code=400, detail="Không thể trích xuất văn bản từ PDF")
            
        # Chấm điểm
        result = engine.evaluate(company_name, year, text)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý file: {str(e)}")
    finally:
        # Dọn dẹp file tạm
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

