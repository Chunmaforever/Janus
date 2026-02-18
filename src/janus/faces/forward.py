from typing import List, Dict, Any
from ..core.parser import ClaimDecomposer
from ..core.puzzle import PuzzleMatcher
from ..agents.searcher import PatentSearcher

class JanusForward:
    """
    Implements the 'Attack' mode (Infringement Search).
    Target: B's patents filed AFTER A's priority date.
    Goal: Find if B is using A's technology (a+b+c).
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.decomposer = ClaimDecomposer()
        # Initialize scorer via PuzzleMatcher's internal scorer or pass explicit config if needed
        # For simplicity, re-instantiating Scorer inside PuzzleMatcher
        from ..core.scorer import RiskScorer
        self.scorer = RiskScorer(config)
        self.matcher = PuzzleMatcher(self.decomposer, self.scorer)
        self.searcher = PatentSearcher(config)
        self.target_patent_date = config.get('target', {}).get('priority_date', '2021-01-01')

    def run_analysis(self, target_claim_text: str, competitor_name: str) -> Dict[str, Any]:
        """
        Executes the forward analysis pipeline.
        
        1. Parse A's claim.
        2. Search B's patents (filter by date >= A's priority date).
        3. Run Puzzle Matcher.
        4. Generate Report Data.
        """
        # 1. Parse Claim
        elements = self.decomposer.decompose(target_claim_text)
        
        # 2. Search Competitor Patents
        # In a real scenario, we'd query by date. 
        # Here we fetch all and filter in Python for demonstration.
        b_patents = self.searcher.get_patents_by_assignee(competitor_name)
        
        # Filter: Keep only patents AFTER target priority date (Potential Infringers)
        potential_infringers = [
            p for p in b_patents 
            if p.get('date', '1900-01-01') >= self.target_patent_date
        ]
        
        if not potential_infringers:
            return {
                "status": "No potential infringers found based on date.",
                "risk_score": 0.0,
                "details": {}
            }
            
        # 3. Match
        match_result = self.matcher.match_elements(elements, potential_infringers)
        
        # 4. Result Construction
        return {
            "mode": "Forward (Infringement Search)",
            "target_claim": target_claim_text,
            "competitor_patents_scanned": len(potential_infringers),
            "match_analysis": match_result
        }
