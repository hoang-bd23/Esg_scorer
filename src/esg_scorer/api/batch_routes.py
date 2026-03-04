import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, Form, BackgroundTasks, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional

import json
import concurrent.futures
from ..models.database import get_db, DBBatchJob, DBCompanyResult
from ..services.batch_service import BatchScoringService
router = APIRouter(tags=["Batch"])
templates = Jinja2Templates(directory="src/esg_scorer/web/templates")

# Thư mục tạm lưu file upload
UPLOAD_DIR = Path("batch_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def update_progress(job_dir: Path, filename: str, status: str):
    progress_file = job_dir / "progress.json"
    if progress_file.exists():
        try:
            with open(progress_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "files" in data:
                data["files"][filename] = status
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception:
            pass

def background_batch_process(job_id: str, folder_path: str):
    db_generator = get_db()
    db = next(db_generator)
    job_dir = Path(folder_path)
    
    try:
        service = BatchScoringService(use_cache=False)
        pdf_files = list(job_dir.glob("*.pdf"))
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            future_to_filename = {}
            for p in pdf_files:
                future = executor.submit(BatchScoringService._process_single_file, str(p), False)
                future_to_filename[future] = p.name
                
            for future in concurrent.futures.as_completed(future_to_filename):
                filename = future_to_filename[future]
                try:
                    result = future.result()
                    if result:
                        db_record = DBCompanyResult(
                            company_name=result.company_name,
                            year=result.year,
                            e_score=result.e_score,
                            s_score=result.s_score,
                            g_score=result.g_score,
                            total_esg_score=result.total_esg_score,
                            details=result.model_dump_json(),
                            batch_job_id=job_id
                        )
                        db.add(db_record)
                        update_progress(job_dir, filename, "completed")
                    else:
                        update_progress(job_dir, filename, "error")
                except Exception as e:
                    update_progress(job_dir, filename, "error")
                    
                # Cập nhật số lượng file đã xử lý ngay khi xong
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
        # Xóa thư mục tạm (bỏ qua lỗi nếu file đang bị khóa trên Windows)
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path, ignore_errors=True)
        except Exception:
            pass
        db.close()

@router.post("/batch-upload", response_class=HTMLResponse)
async def upload_batch_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(..., description="Chon một folder các file pdf")
):
    job_id = str(uuid.uuid4())
    job_dir = UPLOAD_DIR / job_id
    job_dir.mkdir()
    
    saved_count = 0
    file_statuses = {}
    for file in files:
        if file.filename and file.filename.endswith(".pdf"):
            safe_name = file.filename.replace("/", "_").replace("\\", "_")
            file_path = job_dir / safe_name
            with open(file_path, "wb") as f:
                f.write(await file.read())
            file_statuses[safe_name] = "pending"
            saved_count += 1
            
    if saved_count == 0:
        return HTMLResponse(content="<h3>Không có file PDF nào được chọn!</h3>", status_code=400)
        
    # Lưu file progress.json
    progress_file = job_dir / "progress.json"
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump({"files": file_statuses}, f)

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
    background_tasks.add_task(background_batch_process, job_id, str(job_dir))
    
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
        progress_data = {}
        progress_file = UPLOAD_DIR / job_id / "progress.json"
        if progress_file.exists():
            try:
                with open(progress_file, "r", encoding="utf-8") as f:
                    progress_data = json.load(f)
            except: pass
            
        return {
            "id": job.id,
            "total_files": job.total_files,
            "processed_files": job.processed_files,
            "status": job.status,
            "file_details": progress_data.get("files", {})
        }
    finally:
        db.close()

@router.get("/batch-export/{job_id}")
async def export_batch_results(job_id: str):
    from ..services.export_service import ExcelExporter
    from ..models.schemas import CompanyESGResult
    
    db_generator = get_db()
    db = next(db_generator)
    try:
        job = db.query(DBBatchJob).filter(DBBatchJob.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Batch job not found")
            
        records = db.query(DBCompanyResult).filter(DBCompanyResult.batch_job_id == job_id).all()
        if not records:
            raise HTTPException(status_code=404, detail="No results found for this batch")
            
        results = []
        for r in records:
            if r.details:
                try:
                    results.append(CompanyESGResult.model_validate_json(r.details))
                except Exception:
                    pass
                    
        if not results:
            raise HTTPException(status_code=400, detail="Failed to parse results data")
            
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)
        file_path = export_dir / f"batch_export_{job_id}.xlsx"
        
        ExcelExporter.export_batch_results(results, str(file_path))
        
        return FileResponse(
            path=file_path, 
            filename=f"ESG_Batch_Results_{job_id[:8]}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    finally:
        db.close()
