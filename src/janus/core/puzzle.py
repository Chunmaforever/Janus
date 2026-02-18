from typing import List, Dict, Any, Tuple
from .parser import ClaimDecomposer
from .scorer import RiskScorer

class PuzzleMatcher:
    """
    The core engine that matches disjoint patent elements from B to A's claim puzzle.
    """
    
    def __init__(self, decomposer: ClaimDecomposer, scorer: RiskScorer, llm_client=None):
        self.decomposer = decomposer
        self.scorer = scorer
        self.llm_client = llm_client
        
    def match_elements(self, target_elements: List[Dict[str, Any]], reference_patents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Scans reference patents to find matches for each target element.
        
        Args:
            target_elements: Decomposed elements of A's claim.
            reference_patents: List of B's patents (dict with 'id', 'text', 'date', etc.).
            
        Returns:
            Dict: Analysis result containing matches, missing elements, and risk score.
        """
        matches = {} # element_id -> List[patent_id]
        
        # 1. Scanning Pass (Simulated)
        # in real implementation, this would use embeddings or LLM to semantic match
        for element in target_elements:
            el_id = element['id']
            el_text = element['text']
            
            matches[el_id] = []
            
            for patent in reference_patents:
                # Placeholder for semantic search: simple keyword matching for now
                if self._basic_text_match(el_text, patent['text']):
                    matches[el_id].append(patent['id'])
                    
        # 2. Risk Calculation
        found_element_ids = [eid for eid, pids in matches.items() if pids]
        risk_score = self.scorer.calculate_risk_score(found_element_ids, target_elements)
        risk_level = self.scorer.categorize_risk(risk_score)
        
        return {
            "matches": matches,
            "found_elements": found_element_ids,
            "missing_elements": [e['id'] for e in target_elements if e['id'] not in found_element_ids],
            "risk_score": risk_score,
            "risk_level": risk_level
        }

    def _basic_text_match(self, element_text: str, document_text: str) -> bool:
        """
        Simple containment check. Replace with Vector DB or LLM evaluator.
        """
        # A very naive check - split element into significant words
        # and check if a threshold of them appear in doc.
        # This is just for skeleton purposes.
        keywords = [w for w in element_text.split() if len(w) > 3]
        if not keywords:
            return False
            
        hits = 0
        for kw in keywords:
            if kw.lower() in document_text.lower():
                hits += 1
                
        # If > 50% of significant words match, consider it a hit (Simulated)
        return (hits / len(keywords)) > 0.5
