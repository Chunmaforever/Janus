"""
USPTO PatentsView API Integration Test
Tests the connection structure and mapping logic in PatentSearcher.
"""

import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.agents.searcher import PatentSearcher

def test_uspto_structure():
    print("\n=== Testing USPTO PatentsView API Structure ===")
    
    config = {"search": {"source": "patentsview"}}
    searcher = PatentSearcher(config)
    
    # Test 1: Assignee Search (Currently falls back to enriched mock)
    print("\n[Test 1] Assignee Search for 'IBM'")
    results = searcher.get_patents_by_assignee("IBM")
    
    print(f"  Found {len(results)} patents.")
    for p in results[:2]:
        print(f"  - ID: {p['id']}, Title: {p['title']}")
        print(f"    Date: {p['date']}")
        print(f"    Snippet: {p['text'][:100]}...")
    
    # Test 2: Mapping Logic
    print("\n[Test 2] Internal Mapping Logic Validation")
    sample_api_response = {
        "patents": [
            {
                "patent_number": "11223344",
                "patent_title": "AI Powered Analysis",
                "patent_date": "2024-02-20",
                "patent_abstract": "A system for analyzing data using neural networks."
            }
        ],
        "total_patent_count": 1
    }
    
    mapped = searcher._map_patentsview_results(sample_api_response)
    print(f"  Mapped results: {mapped}")
    
    assert mapped[0]['id'] == "11223344"
    assert "AI Powered" in mapped[0]['title']
    print("  ✅ Mapping logic verified.")

if __name__ == "__main__":
    try:
        test_uspto_structure()
        print("\n✅ USPTO Integration Structure Test Passed.")
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        sys.exit(1)
