"""
Algolia API client
"""

import requests
from typing import List, Optional, Dict, TypeVar, cast
from ..types.algolia import AlgoliaResponse, CompanyHit, FacetCounts, FacetType
from ..types.company import Company

T = TypeVar('T', bound=Dict[str, int])

class AlgoliaClient:
    """
    Client for interacting with YC's Algolia API
    """
    
    BASE_URL = 'https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries'
    
    def __init__(self):
        self.headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://www.ycombinator.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.ycombinator.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'x-algolia-agent': 'Algolia for JavaScript (3.35.1); Browser; JS Helper (3.16.1)',
            'x-algolia-application-id': '45BWZJ1SGC',
            'x-algolia-api-key': 'MjBjYjRiMzY0NzdhZWY0NjExY2NhZjYxMGIxYjc2MTAwNWFkNTkwNTc4NjgxYjU0YzFhYTY2ZGQ5OGY5NDMxZnJlc3RyaWN0SW5kaWNlcz0lNUIlMjJZQ0NvbXBhbnlfcHJvZHVjdGlvbiUyMiUyQyUyMllDQ29tcGFueV9CeV9MYXVuY2hfRGF0ZV9wcm9kdWN0aW9uJTIyJTVEJnRhZ0ZpbHRlcnM9JTVCJTIyeWNkY19wdWJsaWMlMjIlNUQmYW5hbHl0aWNzVGFncz0lNUIlMjJ5Y2RjJTIyJTVE'
        }

    def _make_request(self, data: dict) -> AlgoliaResponse:
        """
        Make a request to the Algolia API
        """
        response = requests.post(self.BASE_URL, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_companies_by_batch(self, batch: str) -> List[Company]:
        """
        Get all companies from a specific batch
        """
        data = {
            "requests": [{
                "indexName": "YCCompany_production",
                "params": f"facetFilters=%5B%5B%22batch%3A{batch}%22%5D%5D&hitsPerPage=1000"
            }]
        }
        
        response = self._make_request(data)
        hits: List[CompanyHit] = response['results'][0]['hits']
        return [Company.from_hit(hit) for hit in hits]

    def get_facets(self) -> Optional[FacetCounts]:
        """
        Get facets data including batch statistics
        """
        data = {
            "requests": [{
                "indexName": "YCCompany_production",
                "params": "query=&hitsPerPage=1&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&analytics=false&facets=%5B%22top_company%22%2C%22isHiring%22%2C%22nonprofit%22%2C%22batch%22%2C%22industries%22%2C%22subindustry%22%2C%22regions%22%2C%22app_video_public%22%2C%22demo_day_video_public%22%2C%22app_answers%22%2C%22question_answers%22%5D&sortFacetValuesBy=count&maxValuesPerFacet=1000"
            }]
        }
        
        response = self._make_request(data)
        return response['results'][0]['facets']

    def get_facet(self, facet_type: FacetType) -> Dict[str, int]:
        """
        Get a specific facet's data
        
        Args:
            facet_type: The type of facet to retrieve (e.g., "batch", "regions", etc.)
            
        Returns:
            A dictionary mapping facet values to their counts
        """
        facets = self.get_facets()
        if not facets or facet_type not in facets:
            return {}
            
        return facets[facet_type]

    def get_batch_statistics(self) -> Dict[str, int]:
        """
        Get statistics about company batches
        """
        batches = self.get_facet("batch")
        # Filter out "Unspecified" batch
        return {k: v for k, v in batches.items() if k != "Unspecified"} 