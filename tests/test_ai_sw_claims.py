"""
AI/SW Domain Complex Claim Test
Tests Janus with more abstract, functional claims common in software patents.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer
from janus.core.puzzle import PuzzleMatcher
from janus.core.scorer import RiskScorer
from janus.reporters.report_generator import ReportGenerator

def test_ai_sw_scenario():
    print("\n=== Testing AI/SW Complex Claim Scenario ===")
    
    # Target: A complex AI model deployment claim
    AI_CLAIM = (
        "A method for optimizing neural network deployment comprising: "
        "identifying a target hardware architecture; "
        "quantizing model weights based on the hardware architecture's precision limits; "
        "generating a computational graph specialized for individual compute units of the hardware; "
        "and deploying the specialized computational graph to the target hardware."
    )
    
    # Competitor Portfolio with overlapping but scattered features
    COMPETITOR_PORTFOLIO = [
        {
            "id": "US-SW-1",
            "title": "Model Compression Technique",
            "date": "2024-01-05",
            "text": "A method for model weight quantization. Precision limits are considered during the quantization process to maintain accuracy."
        },
        {
            "id": "US-SW-2",
            "title": "GPU Compilation Engine",
            "date": "2023-12-10",
            "text": "Generating specialized computational graphs for specific GPU architectures. The graphs are optimized for SIMD compute units."
        }
    ]
    
    config = {
        "search": {"source": "mock"},
        "target": {"priority_date": "2023-01-01"},
        "weights": {"core_element": 3.0, "common_element": 1.0}
    }
    
    decomposer = ClaimDecomposer()
    elements = decomposer.decompose(AI_CLAIM)
    
    print(f"\n[AI Claim Decomposition]")
    for el in elements:
        p_mark = "[P]" if el.get('preamble') else f"[{el['id']}]"
        print(f"  {p_mark} w={el['weight']}: {el['text'][:80]}...")
    
    scorer = RiskScorer(config)
    matcher = PuzzleMatcher(decomposer, scorer)
    
    result = matcher.match_elements(elements, COMPETITOR_PORTFOLIO)
    
    print(f"\n[Analysis Result]")
    print(f"  Risk Level: {result['risk_level']} ({result['risk_score']:.2%})")
    print(f"  Found Elements: {result['found_elements']}")
    print(f"  Missing Elements: {result['missing_elements']}")
    
    # Detail scores
    details = result.get('match_details', {})
    for eid in result['found_elements']:
        scores = [v for k, v in details.items() if k.startswith(f"{eid}:")]
        print(f"  - Element [{eid}] top score: {max(scores):.3f}")

    # Generate Report
    full_result = {
        "mode": "Forward (AI/SW Scenario)",
        "target_claim": AI_CLAIM,
        "match_analysis": result
    }
    reporter = ReportGenerator()
    path = reporter.generate_report(full_result)
    print(f"\n✅ AI/SW Test Completed. Report: {path}")

if __name__ == "__main__":
    test_ai_sw_scenario()
