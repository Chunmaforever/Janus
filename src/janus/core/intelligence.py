import os
import json
import re
from typing import Dict, Any, List

class AIIntelligence:
    """
    Expert Intelligence Layer for Janus.
    Performs sophisticated reasoning internally without external API keys.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def analyze_match_results(self, match_result: Dict[str, Any], target_claim: str, elements: List[Dict[str, Any]]) -> str:
        """
        Generates advanced reasoning for the match results using internal logic.
        """
        risk_level = match_result.get("risk_level", "LOW")
        found = match_result.get("found_elements", [])
        missing = match_result.get("missing_elements", [])
        details = match_result.get("match_details", {})
        
        # Identify core element if present in elements list
        core_id = next((e['id'] for e in elements if e.get('weight', 0) > 2.0), None)
        is_core_found = core_id in found
        
        opinion_parts = []
        
        # 1. Overall Assessment
        if risk_level in ["CRITICAL", "HIGH"]:
            status = "🚨 [침해/무효 위험 매우 높음]"
            summary = f"본 청구항의 {len(found)}개 요소가 선행기술과 밀접하게 중첩되어 있습니다."
        elif risk_level == "MEDIUM":
            status = "⚠️ [부분적 위험 존재]"
            summary = f"기술적 구성요소 중 일부({len(found)}개)가 선행기술과 유사하나, 중요한 차이점도 발견됩니다."
        else:
            status = "✅ [안전/회피 성공]"
            summary = "대부분의 핵심 구성요소가 선행기술에서 발견되지 않아 리스크가 낮습니다."
            
        opinion_parts.append(f"{status}\n{summary}")
        
        # 2. Key Technical Reasoning
        if is_core_found:
            max_score = max([v for k, v in details.items() if k.startswith(f"{core_id}:")] + [0.0])
            opinion_parts.append(f"🔍 **핵심 요소 분석:** 가장 핵심적인 요소인 [{core_id}]가 높은 유사도({max_score:.2f})로 발견되었습니다. 이는 법률적으로 매우 위협적인 상황입니다.")
        elif core_id:
             opinion_parts.append(f"💡 **회피 전략:** 핵심 요소인 [{core_id}]가 선행기술에서 발견되지 않았습니다. 분석 시 이 부분의 독창성을 강조하는 전략이 유효합니다.")

        # 3. Component Specifics
        if missing:
            opinion_parts.append(f"🛡️ **보완 권고:** 미발견된 {', '.join(missing)} 요소를 더욱 구체화하거나 상위 개념화하여 권리 범위를 명확히 하는 것이 좋습니다.")

        # 4. Global Context
        countries = set()
        for k, v in details.items():
            if v > 0.3: countries.add(k.split(':')[1][:2]) # Simple ID-based country detection
        
        if countries:
            opinion_parts.append(f"🌍 **글로벌 리스크:** {', '.join(countries)} 국가의 특허 데이터가 주요 위험원으로 확인되었습니다.")

        return "\n\n".join(opinion_parts)

    def evaluate_semantic_support(self, element_text: str, paragraph_text: str) -> Dict[str, Any]:
        """
        AI-driven relevance judgment (Semantic Support Analysis).
        Instead of keyword matching, this simulates an AI agent's technical understanding.
        In a real production environment, this would call an LLM API.
        """
        # 1. Check for Reference Numerals (Strong AI heuristic)
        el_numerals = set(re.findall(r'\((\d+)\)', element_text) or re.findall(r'\b(\d{2,3})\b', element_text))
        pg_numerals = set(re.findall(r'\((\d+)\)', paragraph_text) or re.findall(r'\b(\d{2,3})\b', paragraph_text))
        
        common_numerals = el_numerals.intersection(pg_numerals)
        
        # 2. Simulate Semantic Analysis (Synonyms/Context)
        # Using expanded keyword lists to simulate LLM understanding of technical concepts
        tech_concepts = {
            "chamber": ["room", "container", "housing", "vessel", "compartment"],
            "inlet": ["opening", "port", "supply", "feeder", "entrance", "supply port"],
            "plasma": ["ionized gas", "glow discharge", "activated species"],
            "activation": ["excitation", "energizing", "stimulation"],
            "apparatus": ["system", "device", "equipment", "machine"],
            "lighting": ["lamp", "illuminate", "light", "led", "illumination"],
            "device": ["apparatus", "component", "unit", "system", "element"],
        }
        
        el_lower = element_text.lower()
        pg_lower = paragraph_text.lower()
        
        semantic_score = 0.0
        reasoning = []
        
        # Exact word-for-word overlap (baseline)
        el_words = set(re.findall(r'\w+', el_lower))
        pg_words = set(re.findall(r'\w+', pg_lower))
        overlap = el_words.intersection(pg_words)
        if len(overlap) > 1: # More than one word matches
             semantic_score += 0.2
             reasoning.append(f"Basic keyword overlap detected: {list(overlap)[:3]}")

        # Semantic Mapping
        for concept, synonyms in tech_concepts.items():
            # If the concept OR any of its synonyms is in the element
            if concept in el_lower or any(s in el_lower for s in synonyms):
                # Check if the concept OR any of its synonyms is in the paragraph
                if concept in pg_lower or any(s in pg_lower for s in synonyms):
                    semantic_score += 0.4
                    reasoning.append(f"Semantic match found for concept related to '{concept}'.")
        
        # Numeral Match - Very strong indicator of support
        if common_numerals:
            semantic_score += 0.6 # Increased weight for reference numerals
            reasoning.append(f"Strong structural link via reference numeral(s) {common_numerals}.")
        
        # Cap score at 1.0
        final_score = min(1.0, semantic_score)
        
        # Simulate AI "Thought Process" for the report
        if final_score > 0.6:
            verdict = "✅ 기술적 정합성 높음 (구성요소 지지됨)"
        elif final_score > 0.35:
            verdict = "⚠️ 보통/추론적 지지 (용어 차이 검토 필요)"
        else:
            verdict = "❌ 명시적 지지 부족 (리스크 높음)"
            
        return {
            "score": final_score,
            "verdict": verdict,
            "reasoning": "; ".join(dict.fromkeys(reasoning)) if reasoning else "No direct technical overlap found."
        }

    def _extract_numerals(self, text: str) -> List[str]:
        return re.findall(r'\b(\d{2,3})\b', text)
