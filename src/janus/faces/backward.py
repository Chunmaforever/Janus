from typing import List, Dict, Any
from ..core.parser import ClaimDecomposer
from ..core.puzzle import PuzzleMatcher
from ..agents.searcher import PatentSearcher
from ..agents.drafter import ClaimDrafter

class JanusBackward:
    """
    Implements the 'Defense' mode (Validity & Correction).
    Target: B's patents PUBLISHED BEFORE A's priority date (Prior Art).
    Goal: Find if A's claim is invalid and suggest corrections.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.decomposer = ClaimDecomposer()
        from ..core.scorer import RiskScorer
        self.scorer = RiskScorer(config)
        self.matcher = PuzzleMatcher(self.decomposer, self.scorer)
        self.searcher = PatentSearcher(config)
        self.drafter = ClaimDrafter()
        self.target_patent_date = config.get('target', {}).get('priority_date', '2021-01-01')

    def run_analysis(self, target_claim_text: str, competitor_name: str) -> Dict[str, Any]:
        """
        Executes the backward analysis pipeline.
        
        1. Parse A's claim.
        2. Search Prior Art (filter by date < A's priority date).
        3. Run Puzzle Matcher -> Identify Invalidity Risk.
        4. If Risky -> Simulate Correction.
        """
        # 1. Parse Claim
        elements = self.decomposer.decompose(target_claim_text)
        
        # 2. Search Prior Art
        b_patents = self.searcher.get_patents_by_assignee(competitor_name)
        
        prior_art = [
            p for p in b_patents 
            if p.get('date', '9999-12-31') < self.target_patent_date
        ]
        
        if not prior_art:
            return {
                "status": "No prior art found based on date.",
                "risk_score": 0.0,
                "details": {}
            }
            
        # 3. Match (Invalidity Check)
        match_result = self.matcher.match_elements(elements, prior_art)
        
        # 4. Correction Simulation (If High Risk)
        correction_strategy = {}
        if match_result['risk_score'] > 0.5:
            # Logic: Try to find features in spec or dep claims NOT in prior art
            # Simulated safe feature
            safe_feature = "a user interface configured to display results"
            
            # Simple check if safe feature is in prior art (Reuse matcher logic ideally)
            # For skeleton, assume it's safe if not in match_result's found elements (implied)
            
            # Suggest Amendment
            amended_claim = self.drafter.draft_amendment(target_claim_text, [safe_feature])
            
            correction_strategy = {
                "original_risk": "High",
                "suggested_amendment": amended_claim,
                "added_features": [safe_feature],
                "reasoning": "Added feature not found in identified prior art combination."
            }

        return {
            "mode": "Backward (Validity Defense)",
            "target_claim": target_claim_text,
            "prior_art_scanned": len(prior_art),
            "match_analysis": match_result,
            "correction_proposal": correction_strategy
        }
