"""
Dashboard Integration Test
Verifies the generation of the interactive HTML dashboard.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer
from janus.core.puzzle import PuzzleMatcher
from janus.core.scorer import RiskScorer
from janus.agents.searcher import PatentSearcher
from janus.reporters.report_generator import ReportGenerator

def test_dashboard_generation():
    print("\n=== Testing Premium Dashboard Generation ===")
    
    TARGET_CLAIM = (
        "A chemical vapor deposition apparatus comprising: "
        "a reaction chamber; a gas inlet; and a plasma generator "
        "configured to activate a precursor gas."
    )
    
    config = {
        "search": {"source": "mock"},
        "target": {"priority_date": "2022-01-01"},
        "weights": {"core_element": 2.5, "common_element": 1.0}
    }
    
    decomposer = ClaimDecomposer()
    elements = decomposer.decompose(TARGET_CLAIM)
    
    searcher = PatentSearcher(config)
    global_portfolio = searcher.get_patents_by_assignee("GlobalCorp")
    
    scorer = RiskScorer(config)
    matcher = PuzzleMatcher(decomposer, scorer)
    
    # Run matching
    result = matcher.match_elements(elements, global_portfolio, TARGET_CLAIM)
    
    # Generate HTML Dashboard
    reporter = ReportGenerator()
    html_path = reporter.generate_dashboard(result, elements)
    
    print(f"\n✅ Dashboard generated successfully.")
    print(f"   Path: {html_path}")
    
    # Check if file exists and has content
    assert os.path.exists(html_path)
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "JANUS PATENT ANALYTICS" in content
        assert "risk-progress" in content
        assert "puzzle-matrix" in content

    print("✅ Dashboard content verification passed.")

if __name__ == "__main__":
    test_dashboard_generation()
