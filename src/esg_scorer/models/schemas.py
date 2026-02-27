from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class ESGDimension(str, Enum):
    ENVIRONMENT = "E"
    SOCIAL = "S"
    GOVERNANCE = "G"

class ComponentType(str, Enum):
    ENVIRONMENT = "Environment"
    COMMUNITY = "Community"
    EMPLOYEE_RELATIONS = "Employee Relations"
    DIVERSITY = "Diversity"
    CORPORATE_GOVERNANCE = "Corporate Governance"
    PRODUCT_QUALITY = "Product Quality"

    @property
    def dimension(self) -> ESGDimension:
        mapping = {
            ComponentType.ENVIRONMENT: ESGDimension.ENVIRONMENT,
            ComponentType.COMMUNITY: ESGDimension.SOCIAL,
            ComponentType.EMPLOYEE_RELATIONS: ESGDimension.SOCIAL,
            ComponentType.DIVERSITY: ESGDimension.SOCIAL,
            ComponentType.CORPORATE_GOVERNANCE: ESGDimension.GOVERNANCE,
            ComponentType.PRODUCT_QUALITY: ESGDimension.GOVERNANCE,
        }
        return mapping[self]

class EvidenceItem(BaseModel):
    page_num: int = Field(description="Trang chứa bằng chứng")
    text: str = Field(description="Đoạn văn bản trích xuất (ngữ cảnh)")

class ScoreItem(BaseModel):
    id: str = Field(description="Mã định danh (VD: ENV_STR_A)")
    name: str = Field(description="Tên tiêu chí phụ")
    description: str = Field(default="", description="Mô tả tiêu chí")
    score: int = Field(default=0, ge=0, le=1, description="Điểm: 1 (có), 0 (không)")
    evidences: List[EvidenceItem] = Field(default_factory=list, description="Danh sách các bằng chứng tìm được")

class CategoryScore(BaseModel):
    items: List[ScoreItem] = Field(default_factory=list)
    
    @property
    def total_score(self) -> int:
        return sum(item.score for item in self.items)

class ComponentScore(BaseModel):
    name: ComponentType
    strengths: CategoryScore = Field(default_factory=CategoryScore)
    concerns: CategoryScore = Field(default_factory=CategoryScore)

    @property
    def net_score(self) -> int:
        return self.strengths.total_score - self.concerns.total_score

class ESGScoreWeights(BaseModel):
    e_weight: float = Field(default=1.0, description="Trọng số cho Environment")
    s_weight: float = Field(default=1.0, description="Trọng số cho Social")
    g_weight: float = Field(default=1.0, description="Trọng số cho Governance")

class CompanyESGResult(BaseModel):
    company_name: str
    year: int
    components: Dict[str, ComponentScore] = Field(description="Điểm các thành phần (Environment, Community, etc.)")
    
    @property
    def e_score(self) -> float:
        e_comps = [c for c in self.components.values() if c.name.dimension == ESGDimension.ENVIRONMENT]
        if not e_comps: return 0.0
        return sum(c.net_score for c in e_comps)

    @property
    def s_score(self) -> float:
        s_comps = [c for c in self.components.values() if c.name.dimension == ESGDimension.SOCIAL]
        if not s_comps: return 0.0
        return sum(c.net_score for c in s_comps)

    @property
    def g_score(self) -> float:
        g_comps = [c for c in self.components.values() if c.name.dimension == ESGDimension.GOVERNANCE]
        if not g_comps: return 0.0
        return sum(c.net_score for c in g_comps)

    @property
    def total_esg_score(self) -> float:
        # Tổng điểm ESG ròng theo chuẩn KLD = E_net + S_net + G_net
        # Bằng chính là: Tổng điểm Strength (toàn bộ) - Tổng điểm Concern (toàn bộ)
        return self.e_score + self.s_score + self.g_score
