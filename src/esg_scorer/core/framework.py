from typing import Dict, List
from ..models.schemas import ScoreItem, CategoryScore, ComponentScore, ComponentType

def create_empty_category(items_def: List[Dict[str, str]]) -> CategoryScore:
    return CategoryScore(items=[
        ScoreItem(id=item["id"], name=item["name"]) for item in items_def
    ])

# Định nghĩa các tiêu chí Strengths và Concerns cho từng Component dựa trên file PDF
ENVIRONMENT_STRENGTHS = [
    {"id": "ENV_STR_A", "name": "Beneficial Products and Services"},
    {"id": "ENV_STR_B", "name": "Pollution Prevention"},
    {"id": "ENV_STR_C", "name": "Recycling"},
    {"id": "ENV_STR_D", "name": "Clean Energy"},
    {"id": "ENV_STR_G", "name": "Management Systems"},
    {"id": "ENV_STR_X", "name": "Environment Other Strength"}
]

ENVIRONMENT_CONCERNS = [
    {"id": "ENV_CON_A", "name": "Hazardous Waste"},
    {"id": "ENV_CON_B", "name": "Regulatory Problems"},
    {"id": "ENV_CON_C", "name": "Ozone Depleting Chemicals"},
    {"id": "ENV_CON_D", "name": "Substantial Emissions"},
    {"id": "ENV_CON_E", "name": "Agriculture Chemicals"},
    {"id": "ENV_CON_F", "name": "Climate Change"},
    {"id": "ENV_CON_X", "name": "Environment Other Concerns"}
]

COMMUNITY_STRENGTHS = [
    {"id": "COM_STR_A", "name": "Charitable Giving"},
    {"id": "COM_STR_B", "name": "Innovative Giving"},
    {"id": "COM_STR_C", "name": "Support for Housing"},
    {"id": "COM_STR_D", "name": "Support for Education"},
    {"id": "COM_STR_G", "name": "Volunteer Programs"},
    {"id": "COM_STR_X", "name": "Community Other Strengths"}
]

COMMUNITY_CONCERNS = [
    {"id": "COM_CON_A", "name": "Investment Controversies"},
    {"id": "COM_CON_B", "name": "Negative Economic Impact"},
    {"id": "COM_CON_D", "name": "Tax Disputes"},
    {"id": "COM_CON_X", "name": "Community Other Concerns"}
]

EMPLOYEE_RELATIONS_STRENGTHS = [
    {"id": "EMP_STR_A", "name": "Union Relations"},
    {"id": "EMP_STR_C", "name": "Cash Profit Sharing / Employee Involvement"},
    {"id": "EMP_STR_D", "name": "Retirement Benefits Strength D"},
    {"id": "EMP_STR_F", "name": "Retirement Benefits Strength F"},
    {"id": "EMP_STR_G", "name": "Health and Safety Strength"},
    {"id": "EMP_STR_X", "name": "Employee Strengths Other"}
]

EMPLOYEE_RELATIONS_CONCERNS = [
    {"id": "EMP_CON_A", "name": "Health and Safety Concerns A"},
    {"id": "EMP_CON_B", "name": "Health and Safety Concerns B"},
    {"id": "EMP_CON_C", "name": "Retirement Benefits Concern C"},
    {"id": "EMP_CON_D", "name": "Retirement Benefits Concern D"},
    {"id": "EMP_CON_X", "name": "Emp. Relations Other Concerns"}
]

DIVERSITY_STRENGTHS = [
    {"id": "DIV_STR_A", "name": "Board of Directors A"},
    {"id": "DIV_STR_B", "name": "Board of Directors B"},
    {"id": "DIV_STR_C", "name": "Board of Directors C"},
    {"id": "DIV_STR_D", "name": "Work-Life Benefits"},
    {"id": "DIV_STR_E", "name": "Women and Minority Contracting"},
    {"id": "DIV_STR_F", "name": "Employment of the Disabled"},
    {"id": "DIV_STR_G", "name": "Gay and Lesbian Policies"},
    {"id": "DIV_STR_X", "name": "Diversity Other Strengths"}
]

DIVERSITY_CONCERNS = [
    {"id": "DIV_CON_A", "name": "Controversies"},
    {"id": "DIV_CON_B", "name": "Diversity Other Concerns B"},
    {"id": "DIV_CON_X", "name": "Diversity Other Concerns X"}
]

CORPORATE_GOVERNANCE_STRENGTHS = [
    {"id": "CGOV_STR_A", "name": "Limited Compensation"},
    {"id": "CGOV_STR_C", "name": "Ownership Strength"},
    {"id": "CGOV_STR_D", "name": "Transparency Strength"},
    {"id": "CGOV_STR_X", "name": "CG Other Strengths"}
]

CORPORATE_GOVERNANCE_CONCERNS = [
    {"id": "CGOV_CON_B", "name": "High Compensation"},
    {"id": "CGOV_CON_F", "name": "Accounting Concern"},
    {"id": "CGOV_CON_G", "name": "Transparency Concern"},
    {"id": "CGOV_CON_H", "name": "CG Other Concerns H"},
    {"id": "CGOV_CON_X", "name": "CG Other Concerns X"}
]

PRODUCT_QUALITY_STRENGTHS = [
    {"id": "PRO_STR_A", "name": "Quality / R+D-Innovation"},
    {"id": "PRO_STR_B", "name": "Benefits to Economically Disadvantaged B"},
    {"id": "PRO_STR_C", "name": "Benefits to Economically Disadvantaged C"},
    {"id": "PRO_STR_X", "name": "Product Other Strengths"}
]

PRODUCT_QUALITY_CONCERNS = [
    {"id": "PRO_CON_A", "name": "Product Safety"},
    {"id": "PRO_CON_D", "name": "Product Other Concerns D"},
    {"id": "PRO_CON_E", "name": "Product Other Concerns E"},
    {"id": "PRO_CON_X", "name": "Product Other Concerns X"}
]

def initialize_empty_company_result() -> Dict[str, ComponentScore]:
    """Khởi tạo toàn bộ khung điểm rỗng cho một doanh nghiệp mới"""
    return {
        ComponentType.ENVIRONMENT.value: ComponentScore(
            name=ComponentType.ENVIRONMENT,
            strengths=create_empty_category(ENVIRONMENT_STRENGTHS),
            concerns=create_empty_category(ENVIRONMENT_CONCERNS)
        ),
        ComponentType.COMMUNITY.value: ComponentScore(
            name=ComponentType.COMMUNITY,
            strengths=create_empty_category(COMMUNITY_STRENGTHS),
            concerns=create_empty_category(COMMUNITY_CONCERNS)
        ),
        ComponentType.EMPLOYEE_RELATIONS.value: ComponentScore(
            name=ComponentType.EMPLOYEE_RELATIONS,
            strengths=create_empty_category(EMPLOYEE_RELATIONS_STRENGTHS),
            concerns=create_empty_category(EMPLOYEE_RELATIONS_CONCERNS)
        ),
        ComponentType.DIVERSITY.value: ComponentScore(
            name=ComponentType.DIVERSITY,
            strengths=create_empty_category(DIVERSITY_STRENGTHS),
            concerns=create_empty_category(DIVERSITY_CONCERNS)
        ),
        ComponentType.CORPORATE_GOVERNANCE.value: ComponentScore(
            name=ComponentType.CORPORATE_GOVERNANCE,
            strengths=create_empty_category(CORPORATE_GOVERNANCE_STRENGTHS),
            concerns=create_empty_category(CORPORATE_GOVERNANCE_CONCERNS)
        ),
        ComponentType.PRODUCT_QUALITY.value: ComponentScore(
            name=ComponentType.PRODUCT_QUALITY,
            strengths=create_empty_category(PRODUCT_QUALITY_STRENGTHS),
            concerns=create_empty_category(PRODUCT_QUALITY_CONCERNS)
        ),
    }
