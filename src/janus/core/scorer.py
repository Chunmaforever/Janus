from typing import Dict, List, Any

class RiskScorer:
    """
    Calculates risk scores based on how many claim elements of A are found in B's patents.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.weights = config.get('weights', {'core_element': 5.0, 'common_element': 1.0})

    def calculate_risk_score(self, matched_elements: List[str], all_elements: List[Dict[str, Any]]) -> float:
        """
        Calculates a risk score (0.0 to 1.0) based on matched elements.
        FIX: Preamble elements (weight=0) are excluded from scoring.
        """
        total_weight = 0.0
        matched_weight = 0.0

        for element in all_elements:
            weight = element.get('weight', self.weights['common_element'])

            # 📌 FIX: preamble 요소는 점수 계산 제외
            if element.get('preamble') or weight == 0.0:
                continue

            el_id = element['id']
            total_weight += weight

            if el_id in matched_elements:
                matched_weight += weight

        if total_weight == 0:
            return 0.0

        return min(1.0, matched_weight / total_weight)

    def categorize_risk(self, score: float) -> str:
        """
        Categorizes the risk score into a human-readable level.
        FIX: Thresholds recalibrated — MEDIUM now starts at 0.30 (was 0.40).
        Rationale: 5개 요소 중 절반(50%) 매칭 시 ~0.36 → MEDIUM이 올바른 분류.
        """
        if score >= 0.85:
            return "CRITICAL"
        elif score >= 0.60:
            return "HIGH"
        elif score >= 0.30:
            return "MEDIUM"
        else:
            return "LOW"
