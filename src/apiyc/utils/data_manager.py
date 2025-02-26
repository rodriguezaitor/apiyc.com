"""
Data management utilities for caching and persisting API data
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List

from ..types.algolia import FacetType
from ..types.company import Company

class DataManager:
    """
    Manages local data storage and caching for API responses
    """
    
    def __init__(self):
        # Get the package root directory
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.facets_dir = self.data_dir / 'facets'
        self.companies_dir = self.data_dir / 'companies'
        self.metadata_file = self.data_dir / 'metadata.json'
        
        # Ensure directories exist
        self.facets_dir.mkdir(parents=True, exist_ok=True)
        self.companies_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_facet_path(self, facet_type: FacetType) -> Path:
        """Get the path for a facet file"""
        return self.facets_dir / f"{facet_type}.json"

    def _get_batch_path(self, batch: str) -> Path:
        """Get the path for a batch's companies file"""
        return self.companies_dir / f"{batch}.json"
    
    def save_facet(self, facet_type: FacetType, data: Dict[str, int]) -> None:
        """
        Save facet data to a JSON file
        
        Args:
            facet_type: Type of facet (e.g., "batch", "regions")
            data: Facet data to save
        """
        file_path = self._get_facet_path(facet_type)
        with open(file_path, 'w') as f:
            json.dump({
                'data': data,
                'fetched_at': datetime.now().isoformat()
            }, f, indent=2)
    
    def load_facet(self, facet_type: FacetType) -> Optional[Dict[str, int]]:
        """
        Load facet data from a JSON file
        
        Args:
            facet_type: Type of facet to load
            
        Returns:
            Facet data if available, None otherwise
        """
        file_path = self._get_facet_path(facet_type)
        if not file_path.exists():
            return None
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data['data']
        except (json.JSONDecodeError, KeyError):
            return None
    
    def get_facet_fetch_time(self, facet_type: FacetType) -> Optional[datetime]:
        """
        Get the last fetch time for a facet
        
        Args:
            facet_type: Type of facet to check
            
        Returns:
            Datetime of last fetch if available, None otherwise
        """
        file_path = self._get_facet_path(facet_type)
        if not file_path.exists():
            return None
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['fetched_at'])
        except (json.JSONDecodeError, KeyError):
            return None
    
    def should_refresh_facet(self, facet_type: FacetType, max_age: timedelta) -> bool:
        """
        Check if a facet should be refreshed based on its age
        
        Args:
            facet_type: Type of facet to check
            max_age: Maximum allowed age of the data
            
        Returns:
            True if data should be refreshed, False otherwise
        """
        fetch_time = self.get_facet_fetch_time(facet_type)
        if fetch_time is None:
            return True
            
        age = datetime.now() - fetch_time
        return age > max_age

    def save_companies(self, batch: str, companies: List[Company]) -> None:
        """
        Save companies from a batch to a JSON file
        
        Args:
            batch: Batch identifier (e.g., "W25")
            companies: List of companies to save
        """
        file_path = self._get_batch_path(batch)
        with open(file_path, 'w') as f:
            json.dump({
                'data': [company.to_dict() for company in companies],
                'fetched_at': datetime.now().isoformat()
            }, f, indent=2)

    def load_companies(self, batch: str) -> Optional[List[Company]]:
        """
        Load companies from a batch's JSON file
        
        Args:
            batch: Batch identifier to load
            
        Returns:
            List of companies if available, None otherwise
        """
        file_path = self._get_batch_path(batch)
        if not file_path.exists():
            return None
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                companies_data = data['data']
                return [Company.from_dict(company_dict) for company_dict in companies_data]
        except (json.JSONDecodeError, KeyError):
            return None

    def get_companies_fetch_time(self, batch: str) -> Optional[datetime]:
        """
        Get the last fetch time for a batch's companies
        
        Args:
            batch: Batch identifier to check
            
        Returns:
            Datetime of last fetch if available, None otherwise
        """
        file_path = self._get_batch_path(batch)
        if not file_path.exists():
            return None
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['fetched_at'])
        except (json.JSONDecodeError, KeyError):
            return None

    def should_refresh_companies(self, batch: str, max_age: timedelta) -> bool:
        """
        Check if a batch's companies should be refreshed based on age
        
        Args:
            batch: Batch identifier to check
            max_age: Maximum allowed age of the data
            
        Returns:
            True if data should be refreshed, False otherwise
        """
        fetch_time = self.get_companies_fetch_time(batch)
        if fetch_time is None:
            return True
            
        age = datetime.now() - fetch_time
        return age > max_age
    
    def save_metadata(self, version: str) -> None:
        """
        Save metadata about the cached data
        
        Args:
            version: Version of the data format
        """
        with open(self.metadata_file, 'w') as f:
            json.dump({
                'version': version,
                'last_update': datetime.now().isoformat()
            }, f, indent=2)
    
    def get_metadata(self) -> Optional[Dict[str, str]]:
        """
        Get metadata about the cached data
        
        Returns:
            Metadata if available, None otherwise
        """
        if not self.metadata_file.exists():
            return None
            
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None 