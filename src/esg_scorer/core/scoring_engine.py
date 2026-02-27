import re
from typing import Dict, List, Optional, Any
from ..models.schemas import CompanyESGResult, ComponentScore, ComponentType, EvidenceItem
from .framework import initialize_empty_company_result

class KeywordMatcher:
    """Class hỗ trợ tìm kiếm từ khóa trong text với các biểu thức chính quy"""
    
    @staticmethod
    def _create_pattern(keywords: List[str]) -> re.Pattern:
        """Tạo biểu thức chính quy (Regex) từ danh sách từ khóa"""
        # Sắp xếp theo chiều dài giảm dần để ưu tiên match từ dài trước
        sorted_kw = sorted(keywords, key=len, reverse=True)
        # Escape các ký tự đặc biệt nếu có
        escaped_kw = [re.escape(k.lower()) for k in sorted_kw]
        pattern = r'\b(?:' + '|'.join(escaped_kw) + r')\b'
        return re.compile(pattern, re.IGNORECASE)

    @staticmethod
    def _extract_context(text: str, match_iter: iter, window: int = 200) -> Optional[str]:
        """Trích xuất một đoạn văn ngắn (context) xung quanh từ khóa tìm thấy đẩu tiên"""
        try:
            first_match = next(match_iter)
            start = max(0, first_match.start() - window)
            end = min(len(text), first_match.end() + window)
            context = text[start:end].replace('\n', ' ').strip()
            return f"...{context}..."
        except StopIteration:
            return None

class RuleBasedScoringEngine:
    def __init__(self, keyword_dict: Dict[str, List[str]]):
        """
        Khởi tạo Engine với bộ từ điển. 
        keyword_dict map từ ID tiêu chí (vd: ENV_STR_A) sang 1 list các từ khóa.
        """
        self.patterns = {
            criterion_id: KeywordMatcher._create_pattern(keywords)
            for criterion_id, keywords in keyword_dict.items()
        }

    def evaluate(self, company_name: str, year: int, pdf_pages: List[Dict[str, Any]]) -> CompanyESGResult:
        """Thực thi chấm điểm trên danh sách trang (từ file PDF) cho một công ty"""
        
        result = CompanyESGResult(
            company_name=company_name,
            year=year,
            components=initialize_empty_company_result()
        )
        
        # Lowercase một lần để tăng tốc tìm kiếm nếu không dùng regex
        # Nhưng ở đây Regex IgnoreCase sẽ lo. Nên để nguyên text gốc để extract context tốt.
        
        for comp_name, comp_score in result.components.items():
            # Đánh giá Strengths
            for item in comp_score.strengths.items:
                pattern = self.patterns.get(item.id)
                if pattern:
                    found_evidences = []
                    for page in pdf_pages:
                        page_text = page.get("text", "")
                        matches = list(pattern.finditer(page_text))
                        if matches:
                            ext_context = KeywordMatcher._extract_context(page_text, iter(matches))
                            if ext_context:
                                found_evidences.append(EvidenceItem(
                                    page_num=page.get("page_num"),
                                    text=ext_context
                                ))
                            
                    if found_evidences:
                        item.score = 1
                        item.evidences = found_evidences
                        
            # Đánh giá Concerns
            for item in comp_score.concerns.items:
                pattern = self.patterns.get(item.id)
                if pattern:
                    found_evidences = []
                    for page in pdf_pages:
                        page_text = page.get("text", "")
                        matches = list(pattern.finditer(page_text))
                        if matches:
                            ext_context = KeywordMatcher._extract_context(page_text, iter(matches))
                            if ext_context:
                                found_evidences.append(EvidenceItem(
                                    page_num=page.get("page_num"),
                                    text=ext_context
                                ))
                            
                    if found_evidences:
                        item.score = 1
                        item.evidences = found_evidences
                        
        return result
