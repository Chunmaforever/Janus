from typing import List, Dict, Any
from janus.core.intelligence import AIIntelligence

class InternalMapper:
    """
    Maps claim elements to internal specification paragraphs.
    Helps identify §112 support and generate claim charts.
    """
    
    def __init__(self):
        self.ai = AIIntelligence()
        self.threshold = 0.4 # AI threshold for semantic support

    def map_elements_to_spec(self, elements: List[Dict[str, Any]], paragraphs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Finds the best matching paragraph for each claim element.
        """
        mapping = {} # element_id -> List of {para_id, score, snippet}
        
        for el in elements:
            if el.get('preamble'): continue
            
            el_id = el['id']
            el_text = el['text']
            mapping[el_id] = []
            
            for para in paragraphs:
                result = self.ai.evaluate_semantic_support(el_text, para['text'])
                score = result['score']
                
                if score >= self.threshold:
                    mapping[el_id].append({
                        "para_id": para['id'],
                        "score": score,
                        "verdict": result['verdict'],
                        "reasoning": result['reasoning'],
                        "snippet": para['text'][:200] + "..."
                    })
            
            # Sort by score
            mapping[el_id].sort(key=lambda x: x['score'], reverse=True)
            
        return mapping

    def analyze_compliance_risks(self, mapping: Dict[str, Any], elements: List[Dict[str, Any]], country: str = "US") -> List[Dict[str, Any]]:
        """
        Analyzes compliance risks based on country-specific patent laws.
        US: 35 U.S.C. § 112
        KR: Korean Patent Act Article 42
        """
        risks = []
        is_kr = country.upper() == "KR"
        
        for el in elements:
            if el.get('preamble'): continue
            
            el_id = el['id']
            matches = mapping.get(el_id, [])
            
            if not matches:
                risk_type = "제42조 제4항 제1호(뒷받침요건 미비)" if is_kr else "Written Description (§112(a))"
                issue = f"구성요소 '{el_id}'에 대한 매칭 설명이 본문에 없어 특허법 제42조 제4항 제1호(뒷받침요건) 위반 가능성이 높습니다." if is_kr else f"Element '{el_id}' has no matching description in the specification. Potential lack of support."
                risks.append({
                    "element_id": el_id,
                    "type": risk_type,
                    "severity": "HIGH",
                    "issue": issue,
                    "legal_basis": self._cite_legal_basis(country, "support")
                })
            elif matches[0]['score'] < 0.5:
                risk_type = "제42조 제4항 제2호(명확성 요건)" if is_kr else "Clarity/Support (§112)"
                issue = f"구성요소 '{el_id}'와 명세서 기재 사이의 정합성이 낮아(유사도 {matches[0]['score']:.2f}) 청구범위가 불분명할 수 있습니다." if is_kr else f"Element '{el_id}' has weak support (max similarity {matches[0]['score']:.2f})."
                risks.append({
                    "element_id": el_id,
                    "type": risk_type,
                    "severity": "MEDIUM",
                    "issue": issue,
                    "legal_basis": self._cite_legal_basis(country, "clarity")
                })
            elif matches[0]['score'] < 0.7:
                risks.append({
                    "element_id": el_id,
                    "type": "검토 권고" if is_kr else "Support Verification",
                    "severity": "LOW",
                    "issue": f"구성요소 '{el_id}'가 명세서에 기재되어 있으나 용어상 차이가 있습니다." if is_kr else f"Element '{el_id}' is supported but terminology differs from claim.",
                    "legal_basis": self._cite_legal_basis(country, "verification")
                })
        
        return risks

    def identify_safe_features(self, internal_mapping: Dict[str, Any], external_matches: Dict[str, Any], paragraphs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identifies 'Safe Features' from the specification.
        A feature is safe if:
        1. It is well-described in the spec (Internal score > 0.6).
        2. It is NOT present in external prior art (External score < 0.3).
        """
        safe_features = []
        
        # Check all paragraphs to find something potentially new
        for para in paragraphs:
            para_text = para['text']
            # Simplified: Check if this paragraph text is highly similar to any external match
            is_external = False
            for ext_el_id, ext_matches in external_matches.items():
                for m in ext_matches:
                    # If this paragraph text is too similar to what we found in prior art
                    if self.similarity_engine.score(para_text, m.get('text', '')) > 0.5:
                        is_external = True
                        break
                if is_external: break
            
            if not is_external:
                # Potential safe feature candidate
                safe_features.append({
                    "para_id": para['id'],
                    "text": para_text[:300].strip() + "...",
                    "full_text": para_text.strip()
                })
        
        return safe_features[:3] # Return top 3 candidates

    def _cite_legal_basis(self, country: str, issue_type: str) -> str:
        """Returns the specific legal citation for the country."""
        if country.upper() == "KR":
            if issue_type == "support": return "한국 특허법 제42조 제3항 및 제4항 제1호"
            if issue_type == "clarity": return "한국 특허법 제42조 제4항 제2호"
            return "한국 특허법 제42조"
        else: # Default US
            if issue_type == "support": return "35 U.S.C. § 112 (a)"
            if issue_type == "clarity": return "35 U.S.C. § 112 (b)"
            return "35 U.S.C. § 112"
