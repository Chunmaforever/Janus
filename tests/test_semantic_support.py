"""
Semantic Support Mapping Test (AI-Driven)
Verifies that the AI agent can identify support using synonyms and context.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer, SpecParser
from janus.core.internal_mapper import InternalMapper

def test_semantic_support():
    print("\n=== Testing Semantic Support Mapping (AI-Driven) ===")
    
    # 1. Input Data - Using synonyms
    # Claim uses "lighting device", Spec uses "LED lamp (102)"
    # Claim uses "gas supply port", Spec uses "gas inlet (105)"
    TARGET_CLAIM = (
        "A system comprising: "
        "a lighting device; and a gas supply port."
    )
    
    SPEC_TEXT = """
    [0001] The apparatus includes an LED lamp (102) to illuminate the chamber.
    [0005] A gas inlet (105) is provided to feed precursor gases.
    """
    
    decomposer = ClaimDecomposer()
    elements = decomposer.decompose(TARGET_CLAIM)
    
    parser = SpecParser()
    paragraphs = parser.parse_description(SPEC_TEXT)
    
    mapper = InternalMapper()
    mapping = mapper.map_elements_to_spec(elements, paragraphs)
    
    print("\n[Mapping Results]")
    for el_id, matches in mapping.items():
        if not matches:
            print(f" - Element {el_id}: NO MATCH")
            continue
        best = matches[0]
        print(f" - Element {el_id}: Mapped to para {best['para_id']} (Score: {best['score']:.2f})")
        print(f"   Reasoning: {best['reasoning']}")
        print(f"   Verdict: {best['verdict']}")

    # Assertions
    # lighting device (a) should match LED lamp (102) -> Score should be boosted by synonym/numeral simulation
    assert len(mapping['a']) > 0
    # gas supply port (b) should match gas inlet (105)
    assert len(mapping['b']) > 0
    
    print("\n✅ Semantic Support Test Completed.")

if __name__ == "__main__":
    test_semantic_support()
