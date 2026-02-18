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
        
        Args:
            matched_elements (List[str]): List of element IDs (e.g., ['a', 'b']) found in B's portfolio.
            all_elements (List[Dict[str, Any]]): List of all elements from A's claim, with weights.
            
        Returns:
            float: A risk score between 0.0 and 1.0.
        """
        total_weight = 0.0
        matched_weight = 0.0
        
        for element in all_elements:
            el_id = element['id']
            # Use defined weight or default
            weight = element.get('weight', self.weights['common_element'])
            
            # Check if this element is considered "core" (can be defined in element metadata or config)
            # For simplicity, we use the weight directly here.
            
            total_weight += weight
            
            if el_id in matched_elements:
                matched_weight += weight
                
        if total_weight == 0:
            return 0.0
            
        return min(1.0, matched_weight / total_weight)

    def categorize_risk(self, score: float) -> str:
        """
        Categorizes the risk score into a human-readable level.
        """
        if score >= 0.9:
            return "CRITICAL"
        elif score >= 0.7:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
