from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as esg_router
from .api.batch_routes import router as batch_router

from .models.database import init_db
from contextlib import asynccontextmanager

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
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="src/esg_scorer/web/templates")

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

@app.post("/score-view", response_class=HTMLResponse)
async def score_company_html(
    request: Request,
    file: UploadFile = File(..., description="File PDF báo cáo của doanh nghiệp"),
    company_name: str = Form(..., description="Tên doanh nghiệp"),
    year: int = Form(2024, description="Năm báo cáo"),
    weights: str = Form(None, description="Trọng số. VD: 'E=0.4,S=0.3,G=0.3'")
):
    from .api.routes import score_company
    from .models.database import get_db, DBCompanyResult
    try:
        # Tái sử dụng JSON endpoint nhưng render qua HTML
        result = await score_company(file, company_name, year, weights)
        
        # Lưu vào Database
        db_generator = get_db()
        db = next(db_generator)
        try:
            db_record = DBCompanyResult(
                company_name=result.company_name,
                year=result.year,
                e_score=result.e_score * result.weights.e_weight,
                s_score=result.s_score * result.weights.s_weight,
                g_score=result.g_score * result.weights.g_weight,
                total_esg_score=result.total_esg_score,
                details=result.model_dump_json()  # Lưu JSON chi tiết
            )
            # Điền thêm net_score của 6 thành phần
            db.add(db_record)
            db.commit()
            db.refresh(db_record)
        finally:
            db.close()

        return templates.TemplateResponse("result.html", {"request": request, "result": result})
    except Exception as e:
        return HTMLResponse(content=f"<h3>Lỗi: {e}</h3>", status_code=500)

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
