"""
Y Combinator API client
"""

from datetime import timedelta
from typing import List, Dict, Optional, Tuple
from .algolia import AlgoliaClient
from ..types.company import Company
from ..types.algolia import FacetType
from ..utils.data_manager import DataManager

# Default maximum age for cached data
DEFAULT_MAX_AGE = timedelta(hours=24)

class YCClient:
    """
    Client for interacting with Y Combinator's data
    """
    
    def __init__(self):
        self.algolia = AlgoliaClient()
        self.data_manager = DataManager()

    def get_all_data(self, use_cache: bool = True, max_age: Optional[timedelta] = None) -> Tuple[List[Company], Dict[FacetType, Dict[str, int]]]:
        """
        Get all companies from all batches and all facet data
        
        Args:
            use_cache: Whether to use cached data if available
            max_age: Maximum age of cached data before refresh (default: 24 hours)
            
        Returns:
            A tuple containing:
            - List of all companies across all batches
            - Dictionary mapping facet types to their data
            
        Example:
            >>> client = YCClient()
            >>> companies, facets = client.get_all_data()
            >>> print(f"Total companies: {len(companies)}")
            >>> print(f"Companies in US: {facets['regions']['United States']}")
        """
        # Get all facets first to get batch information
        facets = self.algolia.get_facets()
        if not facets:
            return [], {}
            
        # Get all batches
        batches = facets['batch']
        
        # Initialize result containers
        all_companies: List[Company] = []
        all_facets: Dict[FacetType, Dict[str, int]] = {}
        
        # Fetch all companies from each batch
        for batch in batches.keys():
            if batch != "Unspecified":  # Skip unspecified batch
                companies = self.get_companies_by_batch(batch, use_cache=use_cache, max_age=max_age)
                all_companies.extend(companies)
        
        # Fetch all facet data
        for facet_type in facets.keys():
            if isinstance(facet_type, str):  # Type check to satisfy mypy
                facet_data = self.get_facet_data(facet_type, use_cache=use_cache, max_age=max_age)
                all_facets[facet_type] = facet_data
        
        return all_companies, all_facets

    def get_companies_by_batch(self, batch: str, use_cache: bool = True, max_age: Optional[timedelta] = None) -> List[Company]:
        """
        Get all companies from a specific batch
        
        Args:
            batch: Batch identifier (e.g., "W25")
            use_cache: Whether to use cached data if available
            max_age: Maximum age of cached data before refresh (default: 24 hours)
            
        Returns:
            List of companies in the batch
        """
        max_age = max_age or DEFAULT_MAX_AGE
        
        # Try to load from cache if allowed
        if use_cache and not self.data_manager.should_refresh_companies(batch, max_age):
            cached_companies = self.data_manager.load_companies(batch)
            if cached_companies is not None:
                return cached_companies
        
        # Fetch fresh data
        companies = self.algolia.get_companies_by_batch(batch)
        
        # Cache the data
        self.data_manager.save_companies(batch, companies)
        
        return companies

    def refresh_companies(self, batch: str) -> List[Company]:
        """
        Force refresh of companies data for a specific batch
        
        Args:
            batch: Batch identifier to refresh
            
        Returns:
            Updated list of companies
        """
        return self.get_companies_by_batch(batch, use_cache=False)

    def get_batch_statistics(self) -> Dict[str, int]:
        """
        Get statistics about all batches
        """
        return self.algolia.get_batch_statistics()

    def get_facet_data(self, facet_type: FacetType, use_cache: bool = True, max_age: Optional[timedelta] = None) -> Dict[str, int]:
        """
        Get data for a specific facet type
        
        Args:
            facet_type: The type of facet to retrieve (e.g., "batch", "regions", etc.)
            use_cache: Whether to use cached data if available
            max_age: Maximum age of cached data before refresh (default: 24 hours)
            
        Returns:
            A dictionary mapping facet values to their counts
            
        Example:
            >>> client = YCClient()
            >>> regions = client.get_facet_data("regions")
            >>> print(regions)
            {'United States': 3000, 'Europe': 500, ...}
        """
        max_age = max_age or DEFAULT_MAX_AGE
        
        # Try to load from cache if allowed
        if use_cache and not self.data_manager.should_refresh_facet(facet_type, max_age):
            cached_data = self.data_manager.load_facet(facet_type)
            if cached_data is not None:
                return cached_data
        
        # Fetch fresh data
        data = self.algolia.get_facet(facet_type)
        
        # Cache the data
        self.data_manager.save_facet(facet_type, data)
        
        return data

    def fetch_and_save_all_facets(self) -> None:
        """
        Fetch and save all available facet data
        """
        facets = self.algolia.get_facets()
        if not facets:
            return
            
        # Save each facet type
        for facet_type in facets.keys():
            if isinstance(facet_type, str):  # Type check to satisfy mypy
                self.get_facet_data(facet_type, use_cache=False)
        
        # Update metadata
        self.data_manager.save_metadata(version="1.0.0")

    def refresh_facet_data(self, facet_type: FacetType) -> None:
        """
        Force refresh of a specific facet's data
        
        Args:
            facet_type: The type of facet to refresh
        """
        self.get_facet_data(facet_type, use_cache=False)

    def get_company_stats(self) -> Dict[str, int]:
        """
        Get general statistics about companies
        """
        facets = self.algolia.get_facets()
        if not facets:
            return {}

        return {
            'hiring': facets['isHiring'].get('true', 0),
            'top_companies': facets['top_company'].get('true', 0),
            'nonprofit': facets['nonprofit'].get('true', 0),
            'total_companies': sum(self.get_batch_statistics().values())
        } 