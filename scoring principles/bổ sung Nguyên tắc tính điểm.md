
# I. Nguyên tắc tính điểm (Theo tài liệu)

Theo Appendix A:

> ESG_score = Tổng điểm của 6 thành phần
> Điểm mỗi thành phần = Tổng Strength – Tổng Concern 

Các biến phụ thuộc gồm:

* esg_score
* e_comp
* s_comp
* g_comp
* esg_strength
* esg_concern

---

# II. Cấu trúc 6 thành phần KLD

## 1️⃣ ENVIRONMENT (E)

### Strength (6 biến)

* ENV_STR_A – Beneficial Products
* ENV_STR_B – Pollution Prevention
* ENV_STR_C – Recycling
* ENV_STR_D – Clean Energy
* ENV_STR_G – Management Systems
* ENV_STR_X – Environment Other Strength

### Concern (7 biến)

* ENV_CON_A – Hazardous Waste
* ENV_CON_B – Regulatory Problems
* ENV_CON_C – Ozone Depleting Chemicals
* ENV_CON_D – Substantial Emissions
* ENV_CON_E – Agriculture Chemicals
* ENV_CON_F – Climate Change
* ENV_CON_X – Environment Other Concern

### Công thức:

E_comp = (Tổng ENV_STR) – (Tổng ENV_CON)

---

## 2️⃣ COMMUNITY (thuộc S)

Strength (6)
Concern (3)

COM_STR_A … COM_STR_X
COM_CON_A … COM_CON_X

Community_score = ΣCOM_STR – ΣCOM_CON

---

## 3️⃣ EMPLOYEE RELATIONS (thuộc S)

Strength (6)
Concern (5)

EMP_STR_A … EMP_STR_X
EMP_CON_A … EMP_CON_X

Employee_score = ΣEMP_STR – ΣEMP_CON

---

## 4️⃣ DIVERSITY (chia cho S và G)

Strength (8)
Concern (4)

DIV_STR_A … DIV_STR_X
DIV_CON_A … DIV_CON_X

---

## 5️⃣ CORPORATE GOVERNANCE (G)

Strength (4)
Concern (5)

CGOV_STR_A … CGOV_STR_X
CGOV_CON_B … CGOV_CON_X

---

## 6️⃣ PRODUCT QUALITY (G)

Strength (4)
Concern (4)

PRO_STR_A … PRO_STR_X
PRO_CON_A … PRO_CON_X

---

# III. Cách mã hóa dữ liệu (Coding Rule)

Theo KLD:

| Trường hợp  | Giá trị |
| ----------- | ------- |
| Có Strength | 1       |
| Không       | 0       |
| Có Concern  | 1       |
| Không       | 0       |

Không dùng:

* Thang 0–4
* Trọng số
* Chuẩn hóa

---

# IV. Công thức tổng hợp chính xác

### 1️⃣ Tính từng thành phần

Environment = ΣENV_STR – ΣENV_CON
Community = ΣCOM_STR – ΣCOM_CON
Employee = ΣEMP_STR – ΣEMP_CON
Diversity = ΣDIV_STR – ΣDIV_CON
Governance = ΣCGOV_STR – ΣCGOV_CON
Product = ΣPRO_STR – ΣPRO_CON

---

### 2️⃣ Tính E, S, G

Theo tài liệu  :

E_comp = Environment

S_comp = Community + Employee + (phần Diversity thuộc S)

G_comp = Governance + Product + (phần Diversity thuộc G)

(Lưu ý: Diversity được chia cho cả S và G tùy cấu trúc nghiên cứu; nếu không chia thì cộng toàn bộ vào S như nhiều nghiên cứu Việt Nam đang làm.)

---

### 3️⃣ Tính tổng ESG

ESG_score =
Environment

* Community
* Employee
* Diversity
* Governance
* Product

Hoặc đơn giản:

ESG_score = esg_strength – esg_concern

Trong đó:

esg_strength = tổng tất cả Strength
esg_concern = tổng tất cả Concern

---

# V. Phạm vi điểm

Vì mỗi biến chỉ 0 hoặc 1:

* Điểm tối đa = tổng số Strength tối đa
* Điểm tối thiểu = - tổng số Concern tối đa

Ví dụ:
Environment:

* Max = +6
* Min = -7

ESG tổng thể có thể âm hoặc dương.

---

# VI. Quy trình chấm chuẩn học thuật

Bước 1: Đọc báo cáo thường niên
Bước 2: Đối chiếu từng biến KLD
Bước 3: Gán 0/1
Bước 4: Tính Strength – Concern
Bước 5: Tính E_comp, S_comp, G_comp
Bước 6: Tính ESG_score

---

# VII. Kết luận

Bộ khung đúng theo tài liệu gồm:

* 6 thành phần
* 50+ biến nhị phân
* Điểm = Strength – Concern
* Không thêm trọng số
* Không chuẩn hóa
* Không đánh giá chất lượng sâu


