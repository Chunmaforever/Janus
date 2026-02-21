import re
from typing import List, Dict, Any, Optional

# 높은 가중치를 부여할 기능적/혁신적 키워드 (하드웨어 구성 수식어)
_HIGH_WEIGHT_KEYWORDS = [
    "configured to", "adapted to", "operable to",
    "plasma", "generator", "activat",
]
# 낮은 가중치 (일반적인 수동 부품)
_LOW_WEIGHT_KEYWORDS = ["inlet", "outlet", "regulator", "housing", "body"]


class ClaimDecomposer:
    """
    Parses patent claims into preamble + body elements (a, b, c).
    FIX: Preamble is now separated from body before element splitting.
    """

    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    # ── Public API ────────────────────────────────────────────────────────────

    def decompose(self, claim_text: str) -> List[Dict[str, Any]]:
        """
        Decomposes a claim into structured elements.
        """
        if not claim_text or not claim_text.strip():
            return []

        preamble, body = self._split_preamble(claim_text)

        # Split body by ';' (handle trailing 'and' / 'or')
        raw_parts = re.split(r';\s*(?:and\s+)?', body)

        elements = []
        for i, raw in enumerate(raw_parts):
            clean = raw.strip().rstrip('.')
            if not clean:
                continue

            element_id = chr(ord('a') + i)
            weight = self._assign_weight(clean)
            el_type = self._classify_type(clean)

            elements.append({
                'id': element_id,
                'text': clean,
                'weight': weight,
                'type': el_type,
                'preamble': False,
            })

        # Prepend preamble as reference element (not scored)
        if preamble:
            elements.insert(0, {
                'id': 'P',
                'text': preamble,
                'weight': 0.0,   # preamble은 리스크 점수에 미포함
                'type': 'preamble',
                'preamble': True,
            })

        return elements

    def identify_core_element(self, elements: List[Dict[str, Any]]) -> Optional[str]:
        """
        핵심 요소 식별: preamble 제외, 가중치 최고 요소 반환.
        동점이면 더 긴(구체적인) 텍스트를 선택.
        """
        body_els = [e for e in elements if not e.get('preamble')]
        if not body_els:
            return None
        core = max(body_els, key=lambda x: (x['weight'], len(x['text'])))
        return core['id']

    # ── Private helpers ───────────────────────────────────────────────────────

    def _split_preamble(self, claim_text: str):
        """
        'comprising:', 'including:', 'consisting of:' 등을 기준으로
        preamble과 body를 분리한다.
        """
        pattern = re.compile(
            r'^(.*?\b(?:comprising|including|consisting of|having)\s*:?)\s*(.*)',
            re.IGNORECASE | re.DOTALL
        )
        m = pattern.match(claim_text.strip())
        if m:
            return m.group(1).strip(), m.group(2).strip()
        # 분리 기준 없으면 전체를 body로
        return "", claim_text.strip()

    def _assign_weight(self, text: str) -> float:
        """텍스트 특성 기반 가중치 부여 (기능적 요소 우선)."""
        text_lower = text.lower()

        score = 1.0
        for kw in _HIGH_WEIGHT_KEYWORDS:
            if kw in text_lower:
                score += 0.5
        for kw in _LOW_WEIGHT_KEYWORDS:
            if kw in text_lower:
                score -= 0.2
        return max(0.5, round(score, 1))

    def _classify_type(self, text: str) -> str:
        """요소 타입 분류 (placeholder — LLM 연동 후 교체 예정)."""
        text_lower = text.lower()
        if any(k in text_lower for k in ["method", "step", "perform"]):
            return "method_step"
        if any(k in text_lower for k in ["configured to", "operable to", "adapted to"]):
            return "functional_component"
        return "structural_component"


class SpecParser:
    """
    Parses patent specifications (Description/Background) into semantic paragraphs.
    Identifies reference numerals for mapping.
    """
    
    def parse_description(self, text: str) -> List[Dict[str, Any]]:
        """
        Splits text into paragraphs, often demarcated by [0001], [0002] or just newlines.
        """
        if not text:
            return []
            
        # Try to find paragraph numbers [nnnn]
        paragraphs = []
        parts = re.split(r'(\[\d{4}\])', text)
        
        current_id = "General"
        for part in parts:
            if re.match(r'\[\d{4}\]', part):
                current_id = part.strip('[]')
            else:
                content = part.strip()
                if content:
                    paragraphs.append({
                        "id": current_id,
                        "text": content,
                        "numerals": self._extract_numerals(content)
                    })
        
        # Fallback if no [nnnn] format
        if not paragraphs:
            parts = text.split('\n\n')
            for i, part in enumerate(parts):
                content = part.strip()
                if content:
                    paragraphs.append({
                        "id": f"{i+1:04d}",
                        "text": content,
                        "numerals": self._extract_numerals(content)
                    })

        return paragraphs

    def _extract_numerals(self, text: str) -> List[str]:
        """Extracts reference numerals (e.g., 'chamber (102)')"""
        return re.findall(r'\b(\d{2,3})\b', text)
