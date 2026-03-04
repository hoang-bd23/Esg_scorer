import os
import logging
from pathlib import Path
import uuid
import shutil
from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as esg_router
from .api.batch_routes import router as batch_router

from .models.database import init_db
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

# Đường dẫn tuyệt đối tới thư mục templates (không phụ thuộc CWD)
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = str(BASE_DIR / "web" / "templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="ESG Scoring API",
    description="Hệ thống chấm điểm ESG tự động cho doanh nghiệp Việt Nam theo KLD Framework",
    version="0.1.0",
    lifespan=lifespan
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các API routes (JSON)
app.include_router(esg_router, prefix="/api")
app.include_router(batch_router)

# Giao diện Web (UI Routes)
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    from .models.database import get_db, DBCompanyResult
    from sqlalchemy import desc
    
    db_generator = get_db()
    db = next(db_generator)
    try:
        # Lấy top 50 công ty mới nhất hoặc điểm cao nhất
        results = db.query(DBCompanyResult).order_by(desc(DBCompanyResult.total_esg_score)).limit(50).all()
        return templates.TemplateResponse("dashboard.html", {"request": request, "results": results})
    finally:
        db.close()

# Thư mục lưu file tạm đơn lẻ
_PROJECT_ROOT = BASE_DIR.parent.parent
SINGLE_UPLOAD_DIR = _PROJECT_ROOT / "single_uploads"
SINGLE_UPLOAD_DIR.mkdir(exist_ok=True)

def background_score_single(job_id: str, temp_path: str, company_name: str, year: int):
    from .api.routes import engine, extractor
    from .models.database import get_db, DBCompanyResult, DBBatchJob
    
    db_generator = get_db()
    db = next(db_generator)
    try:
        logger.info(f"Background: Bắt đầu xử lý {temp_path} cho {company_name}")
        text = extractor.extract_text(temp_path, use_cache=False)
        if text:
            result = engine.evaluate(company_name, year, text)
            db_record = DBCompanyResult(
                company_name=result.company_name,
                year=result.year,
                e_score=result.e_score,
                s_score=result.s_score,
                g_score=result.g_score,
                total_esg_score=result.total_esg_score,
                details=result.model_dump_json(),
                batch_job_id=job_id  # Liên kết kết quả với job_id này
            )
            db.add(db_record)
            
            job = db.query(DBBatchJob).filter(DBBatchJob.id == job_id).first()
            if job:
                job.status = "completed"
                job.processed_files = 1
            db.commit()
            logger.info(f"Background: Xử lý xong {company_name}")
        else:
            job = db.query(DBBatchJob).filter(DBBatchJob.id == job_id).first()
            if job:
                job.status = "error"
            db.commit()
            logger.error(f"Background: Trích xuất lỗi cho {company_name}")
            
    except Exception as e:
        logger.error(f"Background: Lỗi xử lý single file: {e}", exc_info=True)
        job = db.query(DBBatchJob).filter(DBBatchJob.id == job_id).first()
        if job:
            job.status = "error"
            db.commit()
    finally:
        # Xóa file tạm
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except:
             pass
        db.close()


@app.post("/score-view", response_class=HTMLResponse)
async def score_company_html(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="File PDF báo cáo của doanh nghiệp"),
    company_name: str = Form(..., description="Tên doanh nghiệp"),
    year: int = Form(2024, description="Năm báo cáo")
):
    from .models.database import get_db, DBBatchJob
    try:
        if not file.filename.endswith(".pdf"):
            return HTMLResponse(content="<h3>Chỉ chấp nhận file PDF</h3>", status_code=400)
            
        job_id = str(uuid.uuid4())
        safe_name = file.filename.replace("/", "_").replace("\\", "_")
        temp_path = SINGLE_UPLOAD_DIR / f"{job_id}_{safe_name}"
        
        # Lưu file tải lên máy chủ trước
        with open(temp_path, "wb") as f:
            f.write(await file.read())
            
        logger.info(f"Đã lưu file {file.filename} -> {temp_path}, Job ID: {job_id}")
        
        # Đăng ký job_id vào DB (Sử dụng tạm DBBatchJob để chứa state 1 file)
        db_generator = get_db()
        db = next(db_generator)
        try:
            new_job = DBBatchJob(id=job_id, total_files=1, processed_files=0, status="processing")
            db.add(new_job)
            db.commit()
        finally:
            db.close()
            
        # Ném vào background processing (Không bắt Web chờ)
        background_tasks.add_task(background_score_single, job_id, str(temp_path), company_name, year)
        
        # Chuyển tới màn hình Loading Polling UI
        return RedirectResponse(url=f"/processing/{job_id}", status_code=303)
        
    except Exception as e:
        logger.error(f"Lỗi khi lưu file {file.filename}: {e}", exc_info=True)
        return HTMLResponse(content=f"<h3>Lỗi: {e}</h3>", status_code=500)

@app.get("/processing/{job_id}", response_class=HTMLResponse)
async def processing_page(request: Request, job_id: str):
    """Trang giao diện Loading liên tục check status của job báo cáo."""
    return templates.TemplateResponse("processing.html", {"request": request, "job_id": job_id})

@app.get("/api/processing-status/{job_id}")
async def check_processing_status(job_id: str):
    from .models.database import get_db, DBBatchJob, DBCompanyResult
    db_generator = get_db()
    db = next(db_generator)
    try:
        job = db.query(DBBatchJob).filter(DBBatchJob.id == job_id).first()
        if not job:
            return {"status": "not_found"}
        
        response_data = {"status": job.status}
        if job.status == "completed":
            # Lấy ra Report Result để redirect
            record = db.query(DBCompanyResult).filter(DBCompanyResult.batch_job_id == job_id).first()
            response_data["result_id"] = record.id if record else None
            
        return response_data
    finally:
        db.close()

@app.get("/result/{result_id}", response_class=HTMLResponse)
async def view_result_detail(request: Request, result_id: int):
    from .models.database import get_db, DBCompanyResult
    from .models.schemas import CompanyESGResult
    
    db_generator = get_db()
    db = next(db_generator)
    try:
        record = db.query(DBCompanyResult).filter(DBCompanyResult.id == result_id).first()
        if not record or not record.details:
            return HTMLResponse(content="<h3>Không tìm thấy báo cáo hoặc dữ liệu chi tiết bị thiếu.</h3>", status_code=404)
            
        result = CompanyESGResult.model_validate_json(record.details)
        return templates.TemplateResponse("result.html", {"request": request, "result": result, "record_id": result_id})
    finally:
        db.close()

from fastapi.responses import RedirectResponse

@app.post("/result/{result_id}/delete")
async def delete_result(result_id: int):
    from .models.database import get_db, DBCompanyResult
    db_generator = get_db()
    db = next(db_generator)
    try:
        record = db.query(DBCompanyResult).filter(DBCompanyResult.id == result_id).first()
        if record:
            db.delete(record)
            db.commit()
        return RedirectResponse(url="/", status_code=303)
    finally:
        db.close()
