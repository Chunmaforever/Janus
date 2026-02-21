from typing import Dict, Any, List

class ClaimDrafter:
    """
    Agent responsible for drafting amended claims or suggesting corrections.
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def recommend_strategic_amendment(self, original_claim: str, safe_features: List[Dict[str, Any]], risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Recommends a strategic amendment based on risks and safe features.
        """
        if not safe_features:
            return {
                "amended_claim": original_claim,
                "strategy": "No safe features found for amendment. Consult specification.",
                "reasoning": "Could not find non-obvious description content to add."
            }
            
        # Select the best safe feature (first one)
        best_feature = safe_features[0]
        feature_text = best_feature['full_text']
        
        # Simple extraction of a core sentence from the feature text
        # (Heuristic: take first sentence or first 100 chars)
        sentence = feature_text.split('.')[0].strip()
        
        amended_claim = original_claim.strip()
        if amended_claim.endswith('.'):
            amended_claim = amended_claim[:-1]
            
        amended_text = f"{amended_claim}; wherein the system further comprises {sentence}."
        
        return {
            "amended_claim": amended_text,
            "strategy": f"Add limitation from Para [{best_feature['para_id']}] to overcome prior art.",
            "safe_feature_source": best_feature['para_id'],
            "reasoning": "This feature was found in the specification but has low similarity to detected prior art."
        }
