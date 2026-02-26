import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, Form, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional

from ..models.database import get_db, DBBatchJob, DBCompanyResult
from ..services.batch_service import BatchScoringService
from .routes import parse_weights_api

router = APIRouter(tags=["Batch"])
templates = Jinja2Templates(directory="src/esg_scorer/web/templates")

# Thư mục tạm lưu file upload
UPLOAD_DIR = Path("batch_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def background_batch_process(job_id: str, folder_path: str, weights_str: str):
    db_generator = get_db()
    db = next(db_generator)
    
    try:
        weights = parse_weights_api(weights_str)
        service = BatchScoringService(use_cache=False)
        
        pdf_files = list(Path(folder_path).glob("*.pdf"))
        
        # Chúng ta chạy process_folder nhưng không update được progress trực tiếp
        # Nâng cấp: Tự implement process flow nhỏ ở đây hoặc sửa lại batch_service
        # Tạm thời gọi trực tiếp bằng vòng lặp hoặc chạy một executor tự custom để update db
        
        import concurrent.futures
        
        # Hàm map của executor mong đợi các list args riêng biệt
        paths_list = [str(p) for p in pdf_files]
        weights_list = [weights] * len(pdf_files)
        cache_list = [False] * len(pdf_files)

        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            for future in executor.map(BatchScoringService._process_single_file, paths_list, weights_list, cache_list):
                if future:
                    # Save to DB Result
                    db_record = DBCompanyResult(
                        company_name=future.company_name,
                        year=future.year,
                        e_score=future.e_score * future.weights.e_weight,
                        s_score=future.s_score * future.weights.s_weight,
                        g_score=future.g_score * future.weights.g_weight,
                        total_esg_score=future.total_esg_score,
                        details=future.model_dump_json(),
                        batch_job_id=job_id
                    )
                    db.add(db_record)
                
            # Cập nhật số lượng file đã xử lý
            job = db.query(DBBatchJob).filter(DBBatchJob.id == job_id).first()
            if job:
                job.processed_files += 1
                db.commit()
                
        # Cập nhật trạng thái hoàn thành
        job = db.query(DBBatchJob).filter(DBBatchJob.id == job_id).first()
        if job:
            job.status = "completed"
            db.commit()
            
    except Exception as e:
        job = db.query(DBBatchJob).filter(DBBatchJob.id == job_id).first()
        if job:
            job.status = "error"
            db.commit()
    finally:
        # Xóa thư mục tạm
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        db.close()

@router.post("/batch-upload", response_class=HTMLResponse)
async def upload_batch_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(..., description="Chon một folder các file pdf"),
    weights: str = Form(None)
):
    job_id = str(uuid.uuid4())
    job_dir = UPLOAD_DIR / job_id
    job_dir.mkdir()
    
    saved_count = 0
    for file in files:
        if file.filename and file.filename.endswith(".pdf"):
            file_path = job_dir / Path(file.filename).name
            with open(file_path, "wb") as f:
                f.write(await file.read())
            saved_count += 1
            
    if saved_count == 0:
        return HTMLResponse(content="<h3>Không có file PDF nào được chọn!</h3>", status_code=400)

    # Lưu job vào DB
    db_generator = get_db()
    db = next(db_generator)
    try:
        new_job = DBBatchJob(id=job_id, total_files=saved_count, processed_files=0)
        db.add(new_job)
        db.commit()
    finally:
        db.close()
        
    # Kích hoạt task chạy ẩn
    background_tasks.add_task(background_batch_process, job_id, str(job_dir), weights)
    
    return RedirectResponse(url=f"/batch-status/{job_id}", status_code=303)

@router.get("/batch-status/{job_id}", response_class=HTMLResponse)
async def batch_status_page(request: Request, job_id: str):
    return templates.TemplateResponse("batch_status.html", {"request": request, "job_id": job_id})

@router.get("/api/batch/{job_id}")
async def get_batch_api(job_id: str):
    db_generator = get_db()
    db = next(db_generator)
    try:
        job = db.query(DBBatchJob).filter(DBBatchJob.id == job_id).first()
        if not job:
            return {"error": "Not Found"}
        return {
            "id": job.id,
            "total_files": job.total_files,
            "processed_files": job.processed_files,
            "status": job.status
        }
    finally:
        db.close()
