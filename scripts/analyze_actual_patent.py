import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from janus.core.parser import ClaimDecomposer, SpecParser
from janus.core.internal_mapper import InternalMapper
from janus.reporters.chart_generator import ChartGenerator

# 1. Inputs
CLAIM_TEXT = """
벤젠(Benzene), 톨루엔(Toluen), 아닐린(Aniline) 및 페놀(Phenol) 중 적어도 하나 이상의 유기물을 수용하기 위한 수용부;
상기 수용부에 수용된 상기 유기물을 고속 분사하여 유기물 클러스터를 생성하기 위한 클러스터 생성부;
상기 클러스터 생성부를 통과하여 생성된 유기물 클러스터를 임시적으로 수용하기 위한 광이온화부;
상기 광이온화부로 UV-C 파장 영역의 자외선을 조사함으로써, 광전 효과(photoelectric effect)에 의해 상기 유기물 클러스터를 광이온화(photoionization)시키기 위한 자외선 광원부;
상기 광이온화부의 양측에 마련되어, 상기 광이온화부에 전위차를 제공함으로써, 유기물 클러스터 이온 빔을 생성하기 위한 입구 전극부;
상기 유기물 클러스터 이온 빔의 진행 방향을 기준으로 상기 입구 전극부의 하류 방향에 위치하고, 상기 유기물 클러스터 이온 빔의 클러스터 크기를 조절할 수 있는 매스 게이트; 및
사용자로부터 선택된 상기 유기물 클러스터 이온 빔의 클러스터 크기를 기초로, 상기 자외선 광원부로부터 조사되는 자외선의 조사 시점과, 상기 매스 게이트에서 상기 유기물 클러스터 이온 빔의 통과를 허용하는 활성 전위를 인가하는 활성 시점을 동기화시키기 위한 제어부를 포함하고,
상기 매스 게이트는, 상기 유기물 클러스터 이온 빔의 진행 경로 상에 위치하고, 인가되는 전위의 크기에 따라, 상기 유기물 클러스터 이온 빔의 통과 여부가 조절되는 유기물 클러스터 이온 빔 생성 장치.
"""

with open("scratch/temp_spec_kr10_1986049.txt", "r", encoding="utf-8") as f:
    SPEC_TEXT = f.read()

# 2. Decompose
decomposer = ClaimDecomposer()
elements = decomposer.decompose(CLAIM_TEXT)

# 3. Parse Spec
parser = SpecParser()
paragraphs = parser.parse_description(SPEC_TEXT)

# 4. Map
mapper = InternalMapper()
mapping = mapper.map_elements_to_spec(elements, paragraphs)

# 5. Risks (KR)
risks = mapper.analyze_compliance_risks(mapping, elements, country="KR")

# 6. Generate Chart
reporter = ChartGenerator()
chart_path = reporter.generate_claim_chart(elements, mapping, risks)

print(f"REPORT_PATH:{chart_path}")
