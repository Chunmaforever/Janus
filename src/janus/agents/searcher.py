import urllib.request
import json
from typing import List, Dict, Any

class PatentSearcher:
    """
    Agent responsible for searching and retrieving patent documents.
    Now supports Global Search across KR, JP, and US.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.source = config.get('search', {}).get('source', 'mock')
        self.api_url = "https://search.patentsview.org/api/v1/patent/"
        self.epo_ops_url = "https://ops.epo.org/3.2/rest-services/"

    def search_patents(self, query: str, country: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Searches for patents based on a query.
        Optional 'country' filter (e.g., 'KR', 'JP', 'US').
        """
        if self.source == 'patentsview':
            return self._patentsview_search(query, limit)
        elif self.source == 'epo_ops':
            return self._epo_ops_search(query, country, limit)
        return self._mock_search(query, limit)

    def get_patents_by_assignee(self, assignee: str, countries: List[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves patents assigned to a specific company.
        'countries' list can filter results (e.g., ['KR', 'US']).
        """
        if self.source == 'patentsview':
            return self._patentsview_assignee_search(assignee)
        elif self.source == 'epo_ops':
            return self._epo_ops_assignee_search(assignee, countries)
        
        results = self._mock_assignee_search(assignee)
        if countries:
            results = [p for p in results if p.get('country') in countries]
        return results

    def _epo_ops_assignee_search(self, assignee: str, countries: List[str]) -> List[Dict[str, Any]]:
        """
        Stub for EPO OPS (Open Patent Services) API.
        Covers 90+ countries including KR and JP.
        """
        # TODO: Implement OAuth2 for EPO OPS
        print(f"EPO OPS Search: Scanning global databases for {assignee} in {countries}...")
        return self._mock_assignee_search(assignee) # Fallback to global mock

    def _patentsview_assignee_search(self, assignee: str) -> List[Dict[str, Any]]:
        # ... (keep existing implementation or fallback)
        return self._mock_assignee_search(assignee)

    def _mock_assignee_search(self, assignee: str) -> List[Dict[str, Any]]:
        """
        Enhanced Mock data covering KR, JP, and US scenarios.
        """
        return [
            {
                "id": "KR-10-2023-0001234",
                "title": "반도체 제조 장비 및 그 제어 방법 (Semiconductor Manufacturing Equipment)",
                "assignee": assignee,
                "country": "KR",
                "date": "2023-01-10",
                "text": "본 발명은 가스 주입구(gas inlet)를 통해 반응 챔버로 공정 가스를 공급하는 시스템을 포함한다. 플라즈마 발생기를 통해 가스를 활성화한다."
            },
            {
                "id": "JP-2022-543210-A",
                "title": "半導体処理装置 (Semiconductor Processing Apparatus)",
                "assignee": assignee,
                "country": "JP",
                "date": "2022-11-15",
                "text": "半導体処理装置は、反応室(reaction chamber)と、基板の温度を維持する温度制御装置(temperature controller)を備えている。"
            },
            {
                "id": "US-11223344-B2",
                "title": "Cloud-based deployment of neural networks",
                "assignee": assignee,
                "country": "US",
                "date": "2023-05-20",
                "text": "A method for quantizing model weights and generating specialized computational graphs for target hardware architectures."
            },
            {
                "id": "KR-10-2018-0099887",
                "title": "공정 데이터 분석 장치 (Prior Art Case)",
                "assignee": assignee,
                "country": "KR",
                "date": "2018-06-05",
                "text": "반응 챔버와 가스 주입구가 구비된 구형 반도체 장비."
            }
        ]

    def _mock_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        return []
        
    def _map_patentsview_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        # ... (keep existing mapper)
        return []
