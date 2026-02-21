import os
from datetime import datetime
from typing import Dict, Any, List

class ChartGenerator:
    """
    Generates Claim Charts (Evidence of Support / 112 Analysis).
    """
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_claim_chart(self, elements: List[Dict[str, Any]], mapping: Dict[str, Any], risks: List[Dict[str, Any]]) -> str:
        """
        Creates a Markdown Claim Chart.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"janus_claim_chart_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            country = "KR" if any("제42조" in str(r.get('type','')) for r in risks) else "US"
            title = "📊 Janus Claim Chart (KR 특허법 제42조 정합성 검토)" if country == "KR" else "📊 Janus Claim Chart (§112 Support Mapping)"
            
            f.write(f"# {title}\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            headers = ["Element", "Claim Text", "Spec Support (Evidence)", "Review Opinion (Legal Basis)"]
            f.write(f"| {' | '.join(headers)} |\n")
            f.write(f"|{'|'.join(['---------']*len(headers))}|\n")
            
            risk_map = {r['element_id']: r for r in risks}
            
            for el in elements:
                el_id = el['id']
                el_text = el['text']
                
                if el.get('preamble'):
                    f.write(f"| Preamble | {el_text} | - | N/A |\n")
                    continue
                
                matches = mapping.get(el_id, [])
                if matches:
                    best = matches[0]
                    support = f"**Para [{best['para_id']}]** (Score: {best['score']:.2f})<br>{best['snippet']}"
                else:
                    support = "❌ **NO MATCH FOUND**"
                
                risk_info = risk_map.get(el_id, {"issue": "✅ Supported", "legal_basis": ""})
                compliance = f"**{risk_info.get('severity', 'PASS')}**: {risk_info['issue']}<br><small>{risk_info.get('legal_basis','')}</small>"
                
                f.write(f"| {el_id} | {el_text} | {support} | {compliance} |\n")
                
            f.write(f"\n---\n*This chart maps Claim 1 elements to internal description for §112 compliance.*")
            
        return filepath
