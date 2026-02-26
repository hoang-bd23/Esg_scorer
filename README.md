# HỆ THỐNG CHẤM ĐIỂM ESG (ESG SCORING SYSTEM)

Tài liệu này đóng vai trò là kim chỉ nam cho toàn bộ dự án chấm điểm ESG tự động dựa trên báo cáo thường niên của doanh nghiệp. Nó dành cho các lập trình viên, nhà phát triển AI (như Antigravity) để hiểu và tiếp tục phát triển dự án.

## 1. TỔNG QUAN DỰ ÁN (PROJECT OVERVIEW)

- **Mục tiêu**: Xây dựng một hệ thống số hóa, tự động chấm điểm ESG theo **KLD ESG Framework** cho 700-800 doanh nghiệp tại Việt Nam.
- **Đầu vào (Input)**: File PDF báo cáo thường niên (VD: `SAM_2024.pdf`), Báo cáo phát triển bền vững của doanh nghiệp.
- **Đầu ra (Output)**: Điểm số ESG chi tiết ở 6 khía cạnh: Environment, Community, Employee Relations, Diversity, Corporate Governance, Product Quality. Kết quả có thể xem trên Web Dashboard, xuất ra Excel hoặc PDF.
- **Cách thức chấm điểm**: Hỗ trợ linh hoạt 2 phương pháp:
  1. Dựa trên bộ quy tắc từ khóa / biểu thức chính quy (Rule-based / Keyword matching) - Chạy Offline, Miễn phí.
  2. Dựa trên AI sinh tạo (LLM-powered) - Yêu cầu API Key (OpenAI/Anthropic/Gemini), độ chính xác cao hơn.
- **Trọng số ESG**: Hỗ trợ cả 2 phương án: Theo tỷ lệ đều nhau (Equal weights) hoặc Trọng số điều chỉnh (Custom weights).

## 2. KIẾN TRÚC HỆ THỐNG (ARCHITECTURE)

Dự án sử dụng Python 3.11+, thiết kế theo mô hình Clean Architecture để tách biệt Logic, Core và Giao diện:

- **Core & Domain `src/esg_scorer/core/`**: Chứa định nghĩa KLD Framework, logic trích xuất PDF, engine chấm điểm (Rule-based & LLM-based adapter).
- **API (Backend) `src/esg_scorer/api/`**: Cung cấp giao diện RESTful API thiết kế bằng **FastAPI**, xử lý các yêu cầu từ Web Frontend hoặc các hệ thống khác. Giao tiếp với Client bằng Pydantic schemas.
- **Services `src/esg_scorer/services/`**: Nơi thực hiện các quy trình nghiệp vụ như chấm điểm hàng loạt (Batch scoring), lưu trữ dữ liệu, tạo báo cáo xuất khẩu (Excel/PDF).
- **CLI `src/esg_scorer/cli.py`**: Cung cấp giao diện dòng lệnh dùng thư viện **Typer**, rất tiện lợi để lập trình viên/quản trị viên tự động hóa các thư mục lớn (700-800 file).
- **Web (Frontend) `src/esg_scorer/web/`**: Giao diện người dùng tích hợp sẵn bên trong FastAPI, được render bằng **Jinja2** templates kết hợp với Tailwind CSS/Bootstrap và Chart.js để vẽ bảng, biểu đồ radar/so sánh.
- **Database `data/esg_results.db`**: Hiện tại ưu tiên dùng **SQLite** qua SQLAlchemy ORM để dễ dàng làm việc offline. Dễ dàng nâng cấp lên PostgreSQL nếu triển khai lên server lớn.

## 3. CÁC THƯ VIỆN CHỦ CHỐT (TECH STACK)

- **Ngôn ngữ**: Python 3.11+
- **Backend API**: `FastAPI` + `uvicorn` (Mạnh, nhanh, hỗ trợ async)
- **PDF Extraction**: `pdfplumber` (Chiết xuất text, table từ các báo cáo thường niên, hỗ trợ tiếng Việt ổn định)
- **CLI**: `Typer`
- **ORM & DB**: `SQLAlchemy`, `aiosqlite`
- **Validation**: `Pydantic` v2
- **Data Export**: `openpyxl` (XLSX), `reportlab` (PDF)

## 4. KẾ HOẠCH TRIỂN KHAI (ROADMAP)

Dự án được chia thành 5 Giai đoạn (Phases):
1. **Giai đoạn 1**: Thiết lập cấu trúc dự án dự án Python, Pydantic Schema, Xây dựng PDF Extractor, KLD Core Engine (Rule-based).
2. **Giai đoạn 2**: Xây dựng ứng dụng CLI để nhập 1 file hoặc Batch hàng trăm file. Thêm tính năng xuất Excel tổng hợp.
3. **Giai đoạn 3**: Xây dựng Backend API bằng FastAPI, Database SQLAlchemy, Quản lý background tasks cho batch job.
4. **Giai đoạn 4**: Xây dựng Web Dashboard có chart, giao diện upload các file PDF, xem và so sánh điểm số ESG. Tích hợp AI LLM Model.
5. **Giai đoạn 5**: Viết Test Scripts (Unit/Integration Tests), kiểm thử hệ thống với tập dữ liệu thực (SAM_2024.pdf), Tối ưu hiệu suất.

## 5. HƯỚNG DẪN CÀI ĐẶT & PHÁT TRIỂN TIẾP (SETUP GUIDE)

### Cài đặt môi trường
1. Clone dự án, mở Terminal tại thư mục `f:\A Personal PJ\Esg_score`.
2. Khởi tạo môi trường ảo Python:
   ```bash
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Cài đặt các requirements (sẽ được tạo ra trong quá trình dev):
   ```bash
   pip install -r requirements.txt
   ```

### Chạy hệ thống (Future)
- **Giao diện dòng lệnh (CLI):**
  ```bash
  python src/esg_scorer/cli.py batch "company evaluation document/"
  ```
- **Khởi động Web App / API:**
  ```bash
  uvicorn esg_scorer.main:app --reload
  ```

## 6. LƯU Ý KHI PHÁT TRIỂN (DEVELOPMENT NOTES)

- **Nguyên tắc Clean Code**: Code phải rõ ràng, tuân thủ `PEP 8`. Sử dụng Type Hints (`-> str`, `Optional[int]`) triệt để cho toàn bộ hàm để dễ bảo trì về sau theo quy tắc của Skill `python-patterns`.
- **Cấu trúc Thư mục**: Hãy tuân thủ cấu trúc đã được định hình tại phần Kiến trúc. Tránh nhét tất cả logic vào Web Routes, thay vào đó hãy chuyển xuống Services.
- **Tiếng Việt NLP**: Các file báo cáo thường là tiếng Việt (PDF), chú ý lỗi font, encoding UTF-8, hãy chuẩn hóa text sau khi trích xuất qua `pdfplumber`. Cần một file từ điển Map các từ khoá tiếng Việt (VD: "Quyên góp", "Từ thiện", "Bình đẳng giới") sang các tiêu chí KLD bằng Tiếng Anh.
- **Concurrency**: Việc trích xuất PDF và AI Request rất tốn thời gian. Phải xử lý đa luồng (Async/Multiprocessing) với khối lượng 700-800 file. Khi xử lý batch, dùng hàng đợi (với FastAPI BackgroundTasks hoặc Concurrent Futures).
