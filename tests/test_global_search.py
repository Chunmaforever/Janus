"""
Global Search Integration Test
Tests Janus with patents from multiple countries (KR, JP, US).
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer
from janus.core.puzzle import PuzzleMatcher
from janus.core.scorer import RiskScorer
from janus.agents.searcher import PatentSearcher
from janus.reporters.report_generator import ReportGenerator

def test_global_analysis():
    print("\n=== Testing Global Patent Analysis (KR, JP, US) ===")
    
    # Target: CVD device claim
    TARGET_CLAIM = (
        "A chemical vapor deposition apparatus comprising: "
        "a reaction chamber; a gas inlet; and a plasma generator "
        "configured to activate a precursor gas."
    )
    
    config = {
        "search": {"source": "mock"},
        "target": {"priority_date": "2022-01-01"},
        "weights": {"core_element": 2.0, "common_element": 1.0}
    }
    
    decomposer = ClaimDecomposer()
    elements = decomposer.decompose(TARGET_CLAIM)
    
    searcher = PatentSearcher(config)
    # Get global portfolio
    global_portfolio = searcher.get_patents_by_assignee("GlobalCorp")
    
    print(f"\n[Global Search Results]")
    for p in global_portfolio:
        print(f"  - [{p['country']}] {p['id']}: {p['title']}")
    
    scorer = RiskScorer(config)
    matcher = PuzzleMatcher(decomposer, scorer)
    
    # Forward analysis on global targets (post 2022)
    forward_targets = [p for p in global_portfolio if p['date'] >= config['target']['priority_date']]
    result = matcher.match_elements(elements, forward_targets)
    
    print(f"\n[Global Match Analysis]")
    print(f"  Risk Level: {result['risk_level']} ({result['risk_score']:.2%})")
    print(f"  Matches found in: {result['found_elements']}")
    
    # Check if KR and JP patents were matched
    matched_countries = set()
    for eid, pids in result['matches'].items():
        for pid in pids:
            # Find patent by id to get country
            p = next((p for p in forward_targets if p['id'] == pid), None)
            if p: matched_countries.add(p['country'])
    
    print(f"  Countries contributing to risk: {list(matched_countries)}")
    
    # Generate Global Report
    full_result = {
        "mode": "Forward (Global Search - KR/JP/US)",
        "target_claim": TARGET_CLAIM,
        "match_analysis": result
    }
    reporter = ReportGenerator()
    path = reporter.generate_report(full_result)
    print(f"\n✅ Global Analysis Test Completed. Report: {path}")

if __name__ == "__main__":
    test_global_analysis()
