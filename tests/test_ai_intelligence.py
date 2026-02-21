"""
AI Reasoning Integration Test
Tests the internal "No-API" expert opinion generation.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer
from janus.core.puzzle import PuzzleMatcher
from janus.core.scorer import RiskScorer
from janus.agents.searcher import PatentSearcher
from janus.reporters.report_generator import ReportGenerator

def test_ai_reasoning():
    print("\n=== Testing No-API AI Expert Reasoning ===")
    
    TARGET_CLAIM = (
        "A chemical vapor deposition apparatus comprising: "
        "a reaction chamber; and a plasma generator "
        "configured to activate a precursor gas."
    )
    
    config = {
        "search": {"source": "mock"},
        "target": {"priority_date": "2020-01-01"},
        "weights": {"core_element": 3.0, "common_element": 1.0}
    }
    
    decomposer = ClaimDecomposer()
    elements = decomposer.decompose(TARGET_CLAIM)
    
    # Core element 'b' (plasma generator) has weight 3.0
    
    searcher = PatentSearcher(config)
    # Mock data contains a direct match for plasma generator
    portfolio = searcher.get_patents_by_assignee("TestCorp")
    
    scorer = RiskScorer(config)
    matcher = PuzzleMatcher(decomposer, scorer)
    
    # Run matching with target_claim passed for AI reasoning context
    result = matcher.match_elements(elements, portfolio, TARGET_CLAIM)
    
    print(f"\n[AI Expert Opinion Output]")
    print("-" * 40)
    print(result.get("ai_opinion", "N/A"))
    print("-" * 40)
    
    assert "Expert Opinion" in result.get("ai_opinion", "") or "위험" in result.get("ai_opinion", "")
    print("✅ AI Reasoning generation verified.")

    # Generate Report to verify Markdown section
    reporter = ReportGenerator()
    path = reporter.generate_report({
        "mode": "Forward (AI Intelligence Test)",
        "target_claim": TARGET_CLAIM,
        "match_analysis": result
    })
    print(f"✅ Report generated with AI opinion: {path}")

if __name__ == "__main__":
    test_ai_reasoning()
