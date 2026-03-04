# Danh Sách Từ Khóa Chấm Điểm ESG (KLD Framework)

Hệ thống hiện tại sử dụng phương pháp tìm kiếm từ khóa (Keyword Matching) kết hợp với Regex để bóc tách bằng chứng và tự động chấm điểm. Dưới đây là danh sách toàn bộ các từ khóa đang được cấu hình trong hệ thống (`src/esg_scorer/core/keywords.py`).

## 🌍 Môi trường (Environment)

### 👍 Điểm Cộng (Strengths)
- **Sản phẩm có lợi (ENV_STR_A):** `sản phẩm có lợi`, `thân thiện môi trường`, `eco-friendly`, `beneficial products`, `sản phẩm xanh`, `green product`
- **Ngăn ngừa ô nhiễm (ENV_STR_B):** `ngăn ngừa ô nhiễm`, `giảm thiểu ô nhiễm`, `pollution prevention`, `xử lý nước thải`, `xử lý khí thải`
- **Tái chế & Tuần hoàn (ENV_STR_C):** `tái chế`, `recycling`, `tái sử dụng`, `tuần hoàn`, `kinh tế tuần hoàn`, `circular economy`
- **Năng lượng sạch (ENV_STR_D):** `năng lượng sạch`, `năng lượng tái tạo`, `clean energy`, `mặt trời`, `điện gió`, `solar`, `wind energy`
- **Hệ thống quản lý (ENV_STR_G):** `hệ thống quản lý môi trường`, `ISO 14001`, `environmental management`, `chứng nhận môi trường`
- **Các thế mạnh khác (ENV_STR_X):** `bảo vệ môi trường`, `environmental protection`, `bảo tồn`, `conservation`

### 👎 Điểm Trừ / Rủi ro (Concerns)
- **Chất thải độc hại (ENV_CON_A):** `chất thải độc hại`, `chất thải nguy hại`, `hazardous waste`, `rác thải y tế`
- **Vi phạm môi trường (ENV_CON_B):** `vi phạm môi trường`, `xử phạt môi trường`, `regulatory problems`, `phạt tiền môi trường`
- **Ozone (ENV_CON_C):** `suy giảm tầng ozone`, `ozone depleting`, `khí CFC`
- **Phát thải lớn (ENV_CON_D):** `phát thải lớn`, `phát thải khí nhà kính`, `substantial emissions`, `carbon footprint`, `phát thải CO2`
- **Hóa chất (ENV_CON_E):** `hóa chất nông nghiệp`, `thuốc trừ sâu`, `thuốc bảo vệ thực vật`, `agriculture chemicals`
- **Biến đổi khí hậu (ENV_CON_F):** `biến đổi khí hậu`, `climate change`, `hiệu ứng nhà kính`
- **Các nguy cơ khác (ENV_CON_X):** `vấn đề môi trường khác`, `ô nhiễm`, `pollution`

---

## 🤝 Xã hội (Social)

### 1. Cộng đồng (Community)
**👍 Điểm Cộng:**
- **Từ thiện (COM_STR_A):** `từ thiện`, `quyên góp`, `charitable giving`, `tài trợ`, `ủng hộ`
- **Giải pháp sáng tạo (COM_STR_B):** `giải pháp sáng tạo`, `innovative giving`, `cộng đồng thông minh`
- **Hỗ trợ nhà ở (COM_STR_C):** `hỗ trợ nhà ở`, `xây nhà tình nghĩa`, `nhà ở xã hội`, `support for housing`
- **Hỗ trợ giáo dục (COM_STR_D):** `hỗ trợ giáo dục`, `học bổng`, `trường học`, `support for education`, `tài trợ giáo dục`
- **Tình nguyện (COM_STR_G):** `tình nguyện`, `volunteer`, `chiến dịch tình nguyện`, `tình nguyện viên`
- **Khác (COM_STR_X):** `phát triển cộng đồng`, `community development`, `gắn kết cộng đồng`

**👎 Điểm Trừ:**
- **Tranh cãi đầu tư (COM_CON_A):** `tranh cãi đầu tư`, `investment controversies`, `phản đối dự án`, `cưỡng chế`
- **Tác động kinh tế (COM_CON_B):** `tác động kinh tế tiêu cực`, `negative economic impact`, `thất nghiệp địa phương`
- **Thuế (COM_CON_D):** `tranh chấp thuế`, `tax disputes`, `trốn thuế`, `nợ thuế`, `phạt thuế`
- **Khác (COM_CON_X):** `mâu thuẫn cộng đồng`, `community concerns`

### 2. Quan hệ Lao động (Employee Relations)
**👍 Điểm Cộng:**
- **Công đoàn (EMP_STR_A):** `công đoàn`, `union relations`, `ban chấp hành công đoàn`
- **Chia sẻ lợi nhuận (EMP_STR_C):** `chia sẻ lợi nhuận`, `thưởng cổ phiếu`, `ESOP`, `cash profit sharing`, `employee involvement`
- **Đào tạo (EMP_STR_D):** `đào tạo nhân viên`, `khuyến khích nhân viên`, `chương trình đào tạo`
- **Hưu trí (EMP_STR_F):** `phúc lợi hưu trí`, `lương hưu`, `retirement benefits`, `bảo hiểm hưu trí`
- **An toàn lao động (EMP_STR_G):** `an toàn lao động`, `sức khỏe lao động`, `health and safety`, `khám sức khỏe định kỳ`, `an toàn vệ sinh lao động`
- **Khác (EMP_STR_X):** `phúc lợi khác`, `other employee benefits`, `chăm sóc nhân viên`

**👎 Điểm Trừ:**
- **Đình công (EMP_CON_A):** `đình công`, `bãi công`, `tranh chấp lao động`
- **Tai nạn lao động (EMP_CON_B):** `tai nạn lao động`, `bệnh nghề nghiệp`, `không an toàn lao động`
- **Sa thải biên chế (EMP_CON_C):** `cắt giảm nhân sự`, `sa thải`, `workforce reductions`, `nghỉ việc hàng loạt`, `giảm biên chế`
- **Nợ BHXH/Hưu trí (EMP_CON_D):** `cắt giảm lương hưu`, `nợ bảo hiểm`, `nợ BHXH`
- **Khác (EMP_CON_X):** `khiếu nại lao động`, `employee concerns`

### 3. Đa dạng hóa (Diversity)
**👍 Điểm Cộng:**
- **Ban lãnh đạo (DIV_STR_A, B, C):** `CEO nữ`, `nữ tổng giám đốc`, `cơ hội thăng tiến`, `đề bạt lao động nữ`, `thành viên HĐQT nữ`
- **Cân bằng (DIV_STR_D):** `cân bằng công việc`, `work-life balance`, `chế độ thai sản`, `làm việc linh hoạt`
- **Tôn trọng (DIV_STR_F, G, X):** `lao động khuyết tật`, `chính sách LGBT`, `bình đẳng giới`, `đa dạng`, `diversity`, `hòa nhập`

**👎 Điểm Trừ:**
- **Phân biệt (DIV_CON):** `phân biệt đối xử`, `không bình đẳng`, `bất bình đẳng giới`, `bê bối quấy rối`, `kiện cáo phân biệt`, `thiếu hòa nhập`

### 4. Chất lượng Sản phẩm (Product Quality)
**👍 Điểm Cộng:**
- **Chất lượng/R&D (PRO_STR_A):** `chất lượng`, `ISO 9001`, `quality assurance`, `R&D`, `đổi mới`, `sáng tạo`, `bằng sáng chế`
- **Giá trị Xã hội (PRO_STR_B, C):** `sản phẩm giá rẻ`, `hỗ trợ người nghèo`, `giá ưu đãi`, `giải thưởng sản phẩm`, `sản phẩm tin dùng`

**👎 Điểm Trừ:**
- **Rủi ro (PRO_CON):** `sản phẩm thu hồi`, `lỗi sản phẩm`, `mất an toàn sản phẩm`, `quảng cáo sai sự thật`, `lừa dối khách hàng`, `cạnh tranh không lành mạnh`, `lũng đoạn`, `tẩy chay`

---

## 🏛️ Quản trị (Corporate Governance)

### 👍 Điểm Cộng (Strengths)
- **Thù lao hợp lý (CGOV_STR_A):** `thù lao hợp lý`, `limited compensation`, `lương thưởng minh bạch`
- **Sở hữu (CGOV_STR_C):** `sở hữu minh bạch`, `cơ cấu cổ đông`, `ownership strength`, `cổ đông chiến lược`
- **Minh bạch thông tin (CGOV_STR_D, X):** `minh bạch thông tin`, `transparency`, `công bố thông tin rõ ràng`, `báo cáo minh bạch`, `kiểm soát nội bộ`, `quản trị rủi ro`, `đạo đức kinh doanh`

### 👎 Điểm Trừ / Rủi ro (Concerns)
- **Mức thù lao (CGOV_CON_B):** `thù lao quá cao`, `high compensation`, `lương lãnh đạo bất thường`
- **Xung đột & Kế toán (CGOV_CON_F, G):** `xung đột lợi ích`, `sở hữu chéo`, `giao dịch bên liên quan bất thường`, `sai sót kế toán`, `kiểm toán ngoại trừ`, `không minh bạch tài chính`
- **Bê bối (CGOV_CON_H, X):** `vi phạm công bố thông tin`, `chậm báo cáo`, `che giấu thông tin`, `bê bối lãnh đạo`, `lạm quyền`, `tham nhũng`, `bribery`

---
*Lưu ý: Bạn có thể cập nhật, chỉnh sửa trực tiếp các cụm từ này trong file mã nguồn `src/esg_scorer/core/keywords.py` để hệ thống tự động nhận diện theo chuẩn từ vựng mới của bạn.*
