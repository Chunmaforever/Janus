"""
KR Patent Compliance Test
Verifies the analysis based on KR Patent Act Article 42.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer, SpecParser
from janus.core.internal_mapper import InternalMapper
from janus.reporters.chart_generator import ChartGenerator

def test_kr_compliance():
    print("\n=== Testing KR Patent Compliance (Art. 42) ===")
    
    # 1. Input Data (Korean)
    TARGET_CLAIM = (
        "반도체 증착 장치로서, 반응 챔버; 가스 유입구; 및 전구체 가스를 활성화하도록 구성된 플라즈마 발생기를 포함하는 장치."
    )
    
    # '가스 유입구' is missing in description
    SPEC_TEXT = """
    [0001] 본 발명은 반도체 제조 장치에 관한 것이다.
    [0005] 반응 챔버(100)는 기판을 수용하도록 구비된다.
    [0010] 플라즈마 발생기(200)는 RF 전원을 이용하여 전구체를 활성화한다.
    """
    
    # 2. Decompose Claim
    decomposer = ClaimDecomposer()
    elements = decomposer.decompose(TARGET_CLAIM)
    
    # 3. Parse Specification
    parser = SpecParser()
    paragraphs = parser.parse_description(SPEC_TEXT)
    
    # 4. Run Internal Mapping (Country: KR)
    mapper = InternalMapper()
    mapping = mapper.map_elements_to_spec(elements, paragraphs)
    
    # 5. Analyze Risks (Country: KR)
    risks = mapper.analyze_compliance_risks(mapping, elements, country="KR")
    
    print("\n[KR 기재불비 분석 결과]")
    for risk in risks:
        print(f" - [{risk['severity']}] {risk['type']}: {risk['issue']}")
        print(f"   (법적 근거: {risk['legal_basis']})")
        
    # 6. Generate Chart
    reporter = ChartGenerator()
    chart_path = reporter.generate_claim_chart(elements, mapping, risks)
    
    print(f"\n✅ KR Claim Chart generated: {chart_path}")
    
    # Assertions
    assert any("제42조" in r['type'] for r in risks)
    assert any(r['element_id'] == 'b' and "뒷받침 요건 미비" in r['issue'] for r in risks)
    
    print("\n✅ KR Compliance Test Completed.")

if __name__ == "__main__":
    test_kr_compliance()
