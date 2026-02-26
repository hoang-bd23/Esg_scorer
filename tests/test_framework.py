import pytest
from esg_scorer.core.framework import initialize_empty_company_result
from esg_scorer.core.scoring_engine import RuleBasedScoringEngine, KeywordMatcher
from esg_scorer.models.schemas import ComponentType

def test_initialize_empty_result():
    components = initialize_empty_company_result()
    assert len(components) == 6
    assert ComponentType.ENVIRONMENT.value in components
    
    env_comp = components[ComponentType.ENVIRONMENT.value]
    assert env_comp.name == ComponentType.ENVIRONMENT
    # 6 Strengths, 7 Concerns for Environment theo KLD 
    assert len(env_comp.strengths.items) == 6
    assert len(env_comp.concerns.items) == 7
    
    # Net score ban đầu phải bằng 0
    assert env_comp.net_score == 0

def test_keyword_matcher():
    kw = ["từ thiện", "quyên góp", "charitable giving"]
    pattern = KeywordMatcher._create_pattern(kw)
    
    # Positive case
    assert pattern.search("Công ty đã quyên góp 10 tỷ đồng") is not None
    assert pattern.search("Chương trình charitable giving lớn nhất") is not None
    
    # Negative case
    assert pattern.search("Công ty không làm gì cả") is None

def test_scoring_engine():
    mock_dict = {
        "ENV_STR_A": ["sản phẩm xanh", "eco-friendly"],
        "ENV_CON_A": ["chất thải độc hại"]
    }
    engine = RuleBasedScoringEngine(mock_dict)
    
    text = "Chúng tôi tự hào ra mắt sản phẩm xanh mới. Tuy nhiên năm qua có sự cố tràn chất thải độc hại nhẹ."
    
    result = engine.evaluate("TestCorp", 2024, text)
    env_comp = result.components[ComponentType.ENVIRONMENT.value]
    
    # Phải tìm được cả strength và concern
    assert env_comp.strengths.total_score == 1
    assert env_comp.concerns.total_score == 1
    
    # Điểm Net = 1 - 1 = 0
    assert env_comp.net_score == 0
    
    # Kiểm tra bằng chứng (context)
    strength_item = next(i for i in env_comp.strengths.items if i.id == "ENV_STR_A")
    assert strength_item.score == 1
    assert "sản phẩm xanh" in strength_item.evidence
