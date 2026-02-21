"""
Internal Mapping & §112 Compliance Test
Verifies the ability to map claims to specification and detect deficiencies.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer, SpecParser
from janus.core.internal_mapper import InternalMapper
from janus.reporters.chart_generator import ChartGenerator

def test_internal_mapping():
    print("\n=== Testing Internal Mapping & Claim Chart (§112) ===")
    
    # 1. Input Data
    TARGET_CLAIM = (
        "A chemical vapor deposition apparatus comprising: "
        "a reaction chamber; a gas inlet; and a plasma generator "
        "configured to activate a precursor gas."
    )
    
    # Note: 'gas inlet' is mentioned in claim but lacks description in this mock spec
    SPEC_TEXT = """
    [0001] The present invention relates to a semiconductor manufacturing equipment.
    [0005] A reaction chamber (100) is provided to contain the substrate.
    [0008] A plasma generator (200) is configured to activate a precursor gas using RF power.
    [0012] The precursors are activated into a plasma state to perform deposition.
    """
    
    # 2. Decompose Claim
    decomposer = ClaimDecomposer()
    elements = decomposer.decompose(TARGET_CLAIM)
    print(f"Decomposed into {len(elements)} elements.")
    
    # 3. Parse Specification
    parser = SpecParser()
    paragraphs = parser.parse_description(SPEC_TEXT)
    print(f"Parsed {len(paragraphs)} paragraphs from description.")
    
    # 4. Run Internal Mapping
    mapper = InternalMapper()
    mapping = mapper.map_elements_to_spec(elements, paragraphs)
    
    # 5. Analyze §112 Risks
    risks = mapper.analyze_compliance_risks(mapping, elements)
    
    print("\n[§112 Risk Analysis Results]")
    for risk in risks:
        print(f" - [{risk['severity']}] {risk['type']}: {risk['issue']}")
        
    # 6. Generate Claim Chart
    reporter = ChartGenerator()
    chart_path = reporter.generate_claim_chart(elements, mapping, risks)
    
    print(f"\n✅ Claim Chart generated: {chart_path}")
    
    # Assertions
    # 'reaction chamber' should match para 0005
    assert "0005" in [m['para_id'] for m in mapping.get('a', [])]
    # 'gas inlet' (element b) should have no matches -> HIGH risk
    assert any(r['element_id'] == 'b' and r['severity'] == 'HIGH' for r in risks)
    
    print("\n✅ Internal Mapping & §112 Test Completed.")

if __name__ == "__main__":
    test_internal_mapping()
