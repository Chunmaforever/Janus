"""
Janus 로직 동작 테스트 — 가상 샘플 청구항 사용
시나리오: 반도체 장비 특허 A사 vs 경쟁사 B사
"""

import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer
from janus.core.puzzle import PuzzleMatcher
from janus.core.scorer import RiskScorer
from janus.agents.searcher import PatentSearcher
from janus.agents.drafter import ClaimDrafter
from janus.reporters.report_generator import ReportGenerator

# ─────────────────────────────────────────────
# 📄 샘플 데이터 정의
# ─────────────────────────────────────────────

# A사의 핵심 특허 청구항 (반도체 CVD 장비)
TARGET_CLAIM = (
    "A chemical vapor deposition apparatus comprising: "
    "a reaction chamber configured to receive a substrate; "
    "a gas inlet configured to supply a precursor gas into the reaction chamber; "
    "a plasma generator configured to activate the precursor gas; "
    "a temperature controller configured to maintain a substrate temperature; "
    "and a pressure regulator configured to control chamber pressure."
)

# B사의 특허 포트폴리오 (Mock 데이터 — 실제 API 대체)
COMPETITOR_PATENTS = [
    {
        "id": "KR-B-2021-0012345",
        "title": "CVD 챔버 및 플라즈마 발생 장치",
        "assignee": "B Corp",
        "date": "2022-03-10",
        "text": (
            "본 발명은 반응 챔버(reaction chamber) 내에 기판을 수용하고, "
            "plasma generator를 이용하여 precursor gas를 활성화하는 장치에 관한 것이다. "
            "상기 장치는 gas inlet을 통해 전구체 가스를 공급한다."
        )
    },
    {
        "id": "KR-B-2022-0056789",
        "title": "반도체 공정용 온도 및 압력 제어 시스템",
        "assignee": "B Corp",
        "date": "2023-07-21",
        "text": (
            "A system for semiconductor processing including a temperature controller "
            "to maintain substrate temperature and a pressure regulator to control "
            "chamber pressure during deposition processes."
        )
    },
    {
        "id": "KR-B-2019-0099001",
        "title": "가스 공급 제어 방법",
        "assignee": "B Corp",
        "date": "2019-11-05",
        "text": (
            "A method for controlling gas supply in a deposition system, "
            "wherein a gas inlet supplies process gas to a reaction chamber."
        )
    }
]

# A사 우선일 (Priority Date)
A_PRIORITY_DATE = "2021-06-01"

# Config (API 없이 사용)
CONFIG = {
    "search": {"source": "mock"},
    "target": {"priority_date": A_PRIORITY_DATE},
    "weights": {"core_element": 5.0, "common_element": 1.0}
}

# ─────────────────────────────────────────────
# 🧪 테스트 유틸리티
# ─────────────────────────────────────────────

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_result(label, value):
    print(f"  {label}: {value}")

# ─────────────────────────────────────────────
# 🧩 STEP 1: ClaimDecomposer 테스트
# ─────────────────────────────────────────────

print_section("STEP 1: ClaimDecomposer — 청구항 요소 분해")
decomposer = ClaimDecomposer()
elements = decomposer.decompose(TARGET_CLAIM)

print(f"\n  [입력 청구항]\n  {TARGET_CLAIM}\n")
print(f"  [분해된 요소 — {len(elements)}개]")
for el in elements:
    p_mark = "[P]" if el.get('preamble') else f"[{el['id']}]"
    print(f"    {p_mark} weight={el['weight']:.1f} | {el['text'][:80]}...")

core_id = decomposer.identify_core_element(elements)
print(f"\n  [핵심 요소] → '{core_id}'")

# ─────────────────────────────────────────────
# 🔍 STEP 2: RiskScorer 단독 테스트
# ─────────────────────────────────────────────

print_section("STEP 2: RiskScorer — 리스크 점수 시나리오")
scorer = RiskScorer(CONFIG)

scenarios = [
    ("모든 요소 매칭 (최고 위험)", [e['id'] for e in elements]),
    ("절반 매칭 (중간 위험)", [e['id'] for e in elements[:len(elements)//2]]),
    ("1개만 매칭 (낮은 위험)", [elements[0]['id']]),
    ("매칭 없음 (안전)", []),
]
for label, matched in scenarios:
    score = scorer.calculate_risk_score(matched, elements)
    level = scorer.categorize_risk(score)
    print(f"  {label:30s} → score={score:.2f}  [{level}]")

# ─────────────────────────────────────────────
# ⚔️ STEP 3: Forward Mode — 침해 탐지
# ─────────────────────────────────────────────

print_section("STEP 3: Forward Mode — B사 침해 탐지 (TF-IDF Semantic)")

# 우선일 이후 특허만 필터
infringers = [p for p in COMPETITOR_PATENTS if p['date'] >= A_PRIORITY_DATE]
print(f"  B사 전체 특허: {len(COMPETITOR_PATENTS)}건")
print(f"  A사 우선일({A_PRIORITY_DATE}) 이후 특허: {len(infringers)}건 → 침해 후보")

matcher = PuzzleMatcher(decomposer, scorer)
forward_result = matcher.match_elements(elements, infringers)

print(f"\n  [매칭 결과 (TF-IDF)]")
match_details = forward_result.get('match_details', {})
for el in elements:
    if el.get('preamble'): continue
    el_id = el['id']
    patents = forward_result['matches'].get(el_id, [])
    status = "✅ 발견" if patents else "❌ 미발견"
    
    score_str = ""
    for pid in patents:
        score = match_details.get(f"{el_id}:{pid}", 0.0)
        score_str += f" ({pid}: {score:.3f})"
    
    print(f"    요소 [{el_id}]: {status} {score_str}")

print(f"\n  리스크 점수: {forward_result['risk_score']:.2f} [🚨 {forward_result['risk_level']}]")

# ─────────────────────────────────────────────
# 🛡️ STEP 4: Backward Mode — 무효 방어 + 보정안
# ─────────────────────────────────────────────

print_section("STEP 4: Backward Mode — 선행기술 무효 위험 + 보정안")

# 우선일 이전 특허만 필터
prior_art = [p for p in COMPETITOR_PATENTS if p['date'] < A_PRIORITY_DATE]
print(f"  A사 우선일({A_PRIORITY_DATE}) 이전 선행기술: {len(prior_art)}건")

if prior_art:
    backward_result = matcher.match_elements(elements, prior_art)
    print(f"\n  [선행기술 매칭 결과]")
    for el_id, patents in backward_result['matches'].items():
        status = "⚠️  발견(위험)" if patents else "✅ 안전"
        print(f"    요소 [{el_id}]: {status} {patents if patents else ''}")

    print(f"\n  무효 리스크 점수: {backward_result['risk_score']:.2f}")
    print(f"  무효 리스크 등급: {backward_result['risk_level']}")

    # 리스크가 높으면 보정안 생성
    if backward_result['risk_score'] > 0.3:
        drafter = ClaimDrafter()
        safe_features = [
            "an exhaust system configured to remove reaction by-products from the chamber",
            "a substrate holder configured to rotate the substrate during deposition"
        ]
        amended = drafter.draft_amendment(TARGET_CLAIM, safe_features)
        print(f"\n  [보정 청구항 제안]")
        print(f"  {amended}")
else:
    print("  선행기술 없음 — 무효 위험 없음 ✅")

# ─────────────────────────────────────────────
# 📊 STEP 5: Report Generation
# ─────────────────────────────────────────────
full_forward_result = {
    "mode": "Forward (Infringement Search)",
    "target_claim": TARGET_CLAIM,
    "match_analysis": forward_result
}

reporter = ReportGenerator()
report_path = reporter.generate_report(full_forward_result)
print(f"  리포트 생성 완료: {report_path}")

# ─────────────────────────────────────────────
# 📊 STEP 6: 최종 분석 요약
# ─────────────────────────────────────────────

print_section("STEP 6: 최종 분석 요약")
print(f"""
  📌 대상 특허 (A사)  : CVD 장비 특허 (우선일 {A_PRIORITY_DATE})
  📌 분석 대상 (B사)  : {len(COMPETITOR_PATENTS)}건 특허 포트폴리오

  ⚔️  Forward (침해 탐지)
      - B사 우선일 이후 특허 {len(infringers)}건 스캔
      - 리스크: {forward_result['risk_score']:.0%} [{forward_result['risk_level']}]
      - 발견 요소: {forward_result['found_elements']}

  🛡️  Backward (무효 방어)
      - 선행기술 {len(prior_art)}건 스캔
      - {"보정안 생성 완료" if prior_art and backward_result['risk_score'] > 0.3 else "무효 위험 낮음"}
  
  📌 리포트 파일: {os.path.basename(report_path)}
""")

print("✅ Phase 2 테스트 완료\n")
