from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./esg_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DBCompanyResult(Base):
    __tablename__ = "esg_results"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True, nullable=False)
    year = Column(Integer, index=True, nullable=False)
    
    e_score = Column(Float, default=0.0)
    s_score = Column(Float, default=0.0)
    g_score = Column(Float, default=0.0)
    total_esg_score = Column(Float, default=0.0)
    
    env_net = Column(Integer, default=0)
    com_net = Column(Integer, default=0)
    emp_net = Column(Integer, default=0)
    div_net = Column(Integer, default=0)
    cgov_net = Column(Integer, default=0)
    pro_net = Column(Integer, default=0)
    
    # Lưu toàn bộ model CompanyESGResult dưới dạng JSON string để phục vụ xem chi tiết
    details = Column(String, nullable=True)
    
    # ID của batch job nếu kết quả này thuộc về một batch
    batch_job_id = Column(String, index=True, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class DBBatchJob(Base):
    __tablename__ = "batch_jobs"
    id = Column(String, primary_key=True, index=True)
    total_files = Column(Integer, default=0)
    processed_files = Column(Integer, default=0)
    status = Column(String, default="processing") # processing, completed, error
    created_at = Column(DateTime, default=datetime.utcnow)

