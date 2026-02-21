"""
Claim Drafter Enhancement Test
Verifies 'Safe Feature' extraction and strategic amendment generation.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer, SpecParser
from janus.core.internal_mapper import InternalMapper
from janus.agents.drafter import ClaimDrafter
from janus.reporters.report_generator import ReportGenerator

def test_claim_drafter():
    print("\n=== Testing Claim Drafter Enhancement (Phase 10) ===")
    
    # 1. Inputs
    TARGET_CLAIM = "A bicycle comprising: a frame; and two wheels."
    
    # Mock Description with a 'Safe Feature'
    # Para 0005 matches external prior art (frame)
    # Para 0010 is a new feature (electric motor with solar charging)
    SPEC_TEXT = """
    [0005] The frame (10) is made of carbon fiber to reduce weight.
    [0010] An electric motor (20) is integrated into the rear hub, powered by a solar panel on the frame.
    """
    
    # Mock External Matches (simulating frame is known)
    # matches should be element_id -> list of patent_ids
    EXTERNAL_MATCHES = {
        "a": ["US1234567"]
    }
    MATCH_DETAILS = {
        "a:US1234567": 0.8
    }
    
    # 2. Process
    decomposer = ClaimDecomposer()
    elements = decomposer.decompose(TARGET_CLAIM)
    
    parser = SpecParser()
    paragraphs = parser.parse_description(SPEC_TEXT)
    
    mapper = InternalMapper()
    internal_mapping = mapper.map_elements_to_spec(elements, paragraphs)
    
    # 3. Identify Safe Features
    # Note: identify_safe_features expects external_matches to be the complex dict with 'text'
    # So we provide a compatible dict for the mapper call
    mapper_external_compat = {
        "a": [{"text": "carbon fiber frame for bicycle", "score": 0.8}]
    }
    safe_features = mapper.identify_safe_features(internal_mapping, mapper_external_compat, paragraphs)
    print(f"Found {len(safe_features)} safe features.")
    for sf in safe_features:
        print(f" - Para [{sf['para_id']}]: {sf['text']}")
        
    # 4. Generate Strategic Amendment
    drafter = ClaimDrafter()
    risks = mapper.analyze_compliance_risks(internal_mapping, elements)
    amendment = drafter.recommend_strategic_amendment(TARGET_CLAIM, safe_features, risks)
    
    print("\n[Strategic Amendment Suggestion]")
    print(f"Strategy: {amendment['strategy']}")
    print(f"Amended Claim: {amendment['amended_claim']}")
    
    # 5. Generate Report
    result = {
        "mode": "Forward (Infringement)",
        "target_claim": TARGET_CLAIM,
        "match_analysis": {
            "risk_level": "HIGH",
            "risk_score": 0.85,
            "matches": EXTERNAL_MATCHES,
            "match_details": MATCH_DETAILS
        },
        "amendment_proposal": amendment
    }
    
    reporter = ReportGenerator()
    report_path = reporter.generate_report(result)
    print(f"\n✅ Final Report generated: {report_path}")
    
    # Assertions
    assert "electric motor" in amendment['amended_claim']
    assert "0010" in amendment['strategy']
    
    print("\n✅ Claim Drafter Enhancement Test Completed.")

if __name__ == "__main__":
    test_claim_drafter()
