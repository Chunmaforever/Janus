from janus.core.similarity import TFIDFSimilarity
from janus.core.intelligence import AIIntelligence

class PuzzleMatcher:
    """
    Core engine that coordinates decomposition, matching, and scoring.
    """
    
    def __init__(self, decomposer, scorer):
        self.decomposer = decomposer
        self.scorer = scorer
        self.similarity_engine = TFIDFSimilarity()
        self.intelligence = AIIntelligence()
        self.similarity_threshold = 0.25 # Optimized threshold
        
    def match_elements(self, target_elements: List[Dict[str, Any]], reference_patents: List[Dict[str, Any]], target_claim: str = "") -> Dict[str, Any]:
        """
        Scans reference patents to find matches for each target element.
        FIX: Preamble elements are skipped from matching loop.
        """
        if not target_elements:
            return {
                "matches": {},
                "match_details": {},
                "found_elements": [],
                "missing_elements": [],
                "risk_score": 0.0,
                "risk_level": "LOW",
                "ai_opinion": ""
            }
            
        matches = {}  # element_id -> List[patent_id]
        match_scores = {} # (element_id, patent_id) -> float

        for element in target_elements:
            # 📌 FIX: preamble 요소는 매칭 대상에서 제외
            if element.get('preamble'):
                continue

            el_id = element['id']
            el_text = element['text']
            matches[el_id] = []

            for patent in reference_patents:
                score = self.similarity_engine.score(el_text, patent['text'])
                if score >= self.similarity_threshold:
                    matches[el_id].append(patent['id'])
                    match_scores[(el_id, patent['id'])] = score

        # Risk Calculation (preamble 제외 요소만 사용)
        found_element_ids = [eid for eid, pids in matches.items() if pids]
        risk_score = self.scorer.calculate_risk_score(found_element_ids, target_elements)
        risk_level = self.scorer.categorize_risk(risk_score)

        result = {
            "matches": matches,
            "match_details": {f"{k[0]}:{k[1]}": v for k, v in match_scores.items()},
            "found_elements": found_element_ids,
            "missing_elements": [
                e['id'] for e in target_elements
                if not e.get('preamble') and e['id'] not in found_element_ids
            ],
            "risk_score": risk_score,
            "risk_level": risk_level
        }
        
        # Add AI Reasoning
        result["ai_opinion"] = self.intelligence.analyze_match_results(result, target_claim, target_elements)
        
        return result
