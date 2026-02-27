"""
Từ điển từ khóa cho KLD ESG Framework.
Hỗ trợ cả tiếng Anh và tiếng Việt vì doanh nghiệp VN thường dùng song ngữ hoặc tiếng Việt.
"""

KLD_KEYWORDS = {
    # ENVIRONMENT STRENGTHS
    "ENV_STR_A": ["sản phẩm có lợi", "thân thiện môi trường", "eco-friendly", "beneficial products", "sản phẩm xanh", "green product"],
    "ENV_STR_B": ["ngăn ngừa ô nhiễm", "giảm thiểu ô nhiễm", "pollution prevention", "xử lý nước thải", "xử lý khí thải"],
    "ENV_STR_C": ["tái chế", "recycling", "tái sử dụng", "tuần hoàn", "kinh tế tuần hoàn", "circular economy"],
    "ENV_STR_D": ["năng lượng sạch", "năng lượng tái tạo", "clean energy", "mặt trời", "điện gió", "solar", "wind energy"],
    "ENV_STR_G": ["hệ thống quản lý môi trường", "ISO 14001", "environmental management", "chứng nhận môi trường"],
    "ENV_STR_X": ["bảo vệ môi trường", "environmental protection", "bảo tồn", "conservation"],

    # ENVIRONMENT CONCERNS
    "ENV_CON_A": ["chất thải độc hại", "chất thải nguy hại", "hazardous waste", "rác thải y tế"],
    "ENV_CON_B": ["vi phạm môi trường", "xử phạt môi trường", "regulatory problems", "phạt tiền môi trường"],
    "ENV_CON_C": ["suy giảm tầng ozone", "ozone depleting", "khí CFC"],
    "ENV_CON_D": ["phát thải lớn", "phát thải khí nhà kính", "substantial emissions", "carbon footprint", "phát thải CO2"],
    "ENV_CON_E": ["hóa chất nông nghiệp", "thuốc trừ sâu", "thuốc bảo vệ thực vật", "agriculture chemicals"],
    "ENV_CON_F": ["biến đổi khí hậu", "climate change", "hiệu ứng nhà kính"],
    "ENV_CON_X": ["vấn đề môi trường khác", "ô nhiễm", "pollution"],

    # COMMUNITY STRENGTHS
    "COM_STR_A": ["từ thiện", "quyên góp", "charitable giving", "tài trợ", "ủng hộ"],
    "COM_STR_B": ["giải pháp sáng tạo", "innovative giving", "cộng đồng thông minh"],
    "COM_STR_C": ["hỗ trợ nhà ở", "xây nhà tình nghĩa", "nhà ở xã hội", "support for housing"],
    "COM_STR_D": ["hỗ trợ giáo dục", "học bổng", "trường học", "support for education", "tài trợ giáo dục"],
    "COM_STR_G": ["tình nguyện", "volunteer", "chiến dịch tình nguyện", "tình nguyện viên"],
    "COM_STR_X": ["phát triển cộng đồng", "community development", "gắn kết cộng đồng"],

    # COMMUNITY CONCERNS
    "COM_CON_A": ["tranh cãi đầu tư", "investment controversies", "phản đối dự án", "cưỡng chế"],
    "COM_CON_B": ["tác động kinh tế tiêu cực", "negative economic impact", "thất nghiệp địa phương"],
    "COM_CON_D": ["tranh chấp thuế", "tax disputes", "trốn thuế", "nợ thuế", "phạt thuế"],
    "COM_CON_X": ["mâu thuẫn cộng đồng", "community concerns"],

    # EMPLOYEE RELATIONS STRENGTHS
    "EMP_STR_A": ["công đoàn", "union relations", "ban chấp hành công đoàn"],
    "EMP_STR_C": ["chia sẻ lợi nhuận", "thưởng cổ phiếu", "ESOP", "cash profit sharing", "employee involvement"],
    "EMP_STR_D": ["đào tạo nhân viên", "khuyến khích nhân viên", "chương trình đào tạo", "retirement benefits strength d"],
    "EMP_STR_F": ["phúc lợi hưu trí", "lương hưu", "retirement benefits", "bảo hiểm hưu trí", "retirement benefits strength f"],
    "EMP_STR_G": ["an toàn lao động", "sức khỏe lao động", "health and safety", "khám sức khỏe định kỳ", "an toàn vệ sinh lao động"],
    "EMP_STR_X": ["phúc lợi khác", "other employee benefits", "chăm sóc nhân viên"],

    # EMPLOYEE RELATIONS CONCERNS
    "EMP_CON_A": ["đình công", "bãi công", "tranh chấp lao động", "union relations concerns", "health and safety concerns a"],
    "EMP_CON_B": ["tai nạn lao động", "bệnh nghề nghiệp", "không an toàn lao động", "health and safety concerns b"],
    "EMP_CON_C": ["cắt giảm nhân sự", "sa thải", "workforce reductions", "nghỉ việc hàng loạt", "giảm biên chế", "retirement benefits concern c"],
    "EMP_CON_D": ["cắt giảm lương hưu", "nợ bảo hiểm", "retirement benefits concern d", "nợ BHXH"],
    "EMP_CON_X": ["khiếu nại lao động", "employee concerns"],

    # DIVERSITY STRENGTHS
    "DIV_STR_A": ["CEO nữ", "nữ tổng giám đốc", "phụ nữ lãnh đạo", "board of directors a"],
    "DIV_STR_B": ["thăng tiến công bằng", "cơ hội thăng tiến", "đề bạt lao động nữ", "board of directors b"],
    "DIV_STR_C": ["thành viên HĐQT nữ", "nữ hội đồng quản trị", "phụ nữ trong ban lãnh đạo", "board of directors c"],
    "DIV_STR_D": ["cân bằng công việc", "work-life balance", "chế độ thai sản", "làm việc linh hoạt"],
    "DIV_STR_E": ["hỗ trợ nhóm yếu thế", "ký kết với phụ nữ", "minority contracting"],
    "DIV_STR_F": ["lao động khuyết tật", "người khuyết tật", "employment of disabled"],
    "DIV_STR_G": ["chính sách LGBT", "đồng tính", "gay and lesbian policies"],
    "DIV_STR_X": ["bình đẳng giới", "đa dạng", "diversity", "hòa nhập", "tôn trọng sự khác biệt"],

    # DIVERSITY CONCERNS
    "DIV_CON_A": ["phân biệt đối xử", "không bình đẳng", "non-representation", "bất bình đẳng giới", "controversies"],
    "DIV_CON_B": ["bê bối quấy rối", "kiện cáo phân biệt", "diversity other concerns b"],
    "DIV_CON_X": ["vấn đề đa dạng khác", "thiếu hòa nhập", "diversity other concerns x"],

    # CORPORATE GOVERNANCE STRENGTHS
    "CGOV_STR_A": ["thù lao hợp lý", "limited compensation", "lương thưởng minh bạch"],
    "CGOV_STR_C": ["sở hữu minh bạch", "cơ cấu cổ đông", "ownership strength", "cổ đông chiến lược"],
    "CGOV_STR_D": ["minh bạch thông tin", "transparency", "công bố thông tin rõ ràng", "báo cáo minh bạch"],
    "CGOV_STR_X": ["kiểm soát nội bộ", "quản trị rủi ro", "đạo đức kinh doanh"],

    # CORPORATE GOVERNANCE CONCERNS
    "CGOV_CON_B": ["thù lao quá cao", "high compensation", "lương lãnh đạo bất thường"],
    "CGOV_CON_F": ["xung đột lợi ích", "sở hữu chéo", "accounting concern", "giao dịch bên liên quan bất thường"],
    "CGOV_CON_G": ["sai sót kế toán", "kiểm toán ngoại trừ", "transparency concern", "không minh bạch tài chính"],
    "CGOV_CON_H": ["vi phạm công bố thông tin", "chậm báo cáo", "cg other concerns h", "che giấu thông tin"],
    "CGOV_CON_X": ["bê bối lãnh đạo", "lạm quyền", "tham nhũng", "bribery", "cg other concerns x"],

    # PRODUCT QUALITY STRENGTHS
    "PRO_STR_A": ["chất lượng", "ISO 9001", "chứng nhận chất lượng", "quality assurance", "đảm bảo chất lượng", "R&D", "đổi mới", "sáng tạo", "nghiên cứu và phát triển", "innovation", "bằng sáng chế"],
    "PRO_STR_B": ["sản phẩm giá rẻ", "hỗ trợ người nghèo", "giá ưu đãi", "benefits to economically disadvantaged b"],
    "PRO_STR_C": ["giải thưởng sản phẩm", "sản phẩm tin dùng", "benefits to economically disadvantaged c"],
    "PRO_STR_X": ["product other strengths"],

    # PRODUCT QUALITY CONCERNS
    "PRO_CON_A": ["sản phẩm thu hồi", "lỗi sản phẩm", "mất an toàn sản phẩm", "product safety", "thu hồi sản phẩm"],
    "PRO_CON_D": ["quảng cáo sai sự thật", "lừa dối khách hàng", "product other concerns d", "vi phạm hợp đồng"],
    "PRO_CON_E": ["chống độc quyền", "cạnh tranh không lành mạnh", "antitrust", "lũng đoạn"],
    "PRO_CON_X": ["phàn nàn khách hàng", "khiếu nại sản phẩm", "tẩy chay", "product other concerns x"]
}
