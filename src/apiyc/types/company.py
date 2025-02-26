"""
Company data models
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime

@dataclass
class Company:
    """
    Represents a YC company with all its details
    """
    id: int
    name: str
    slug: str
    website: str
    description: str
    one_liner: str
    batch: str
    status: str
    team_size: int
    industry: str
    subindustry: str
    industries: List[str]
    regions: List[str]
    locations: str
    tags: List[str]
    stage: str
    is_hiring: bool
    is_nonprofit: bool
    is_top_company: bool
    launched_at: Optional[datetime]
    logo_url: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the company instance to a dictionary for JSON serialization
        """
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'website': self.website,
            'description': self.description,
            'one_liner': self.one_liner,
            'batch': self.batch,
            'status': self.status,
            'team_size': self.team_size,
            'industry': self.industry,
            'subindustry': self.subindustry,
            'industries': self.industries,
            'regions': self.regions,
            'locations': self.locations,
            'tags': self.tags,
            'stage': self.stage,
            'is_hiring': self.is_hiring,
            'is_nonprofit': self.is_nonprofit,
            'is_top_company': self.is_top_company,
            'launched_at': self.launched_at.timestamp() if self.launched_at else None,
            'logo_url': self.logo_url
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Company':
        """
        Create a Company instance from a dictionary
        """
        # Convert timestamp back to datetime if present
        launched_at = data.get('launched_at')
        if launched_at is not None:
            launched_at = datetime.fromtimestamp(launched_at)
            
        return cls(
            id=data['id'],
            name=data['name'],
            slug=data['slug'],
            website=data['website'],
            description=data['description'],
            one_liner=data['one_liner'],
            batch=data['batch'],
            status=data['status'],
            team_size=data['team_size'],
            industry=data['industry'],
            subindustry=data['subindustry'],
            industries=data['industries'],
            regions=data['regions'],
            locations=data['locations'],
            tags=data['tags'],
            stage=data['stage'],
            is_hiring=data['is_hiring'],
            is_nonprofit=data['is_nonprofit'],
            is_top_company=data['is_top_company'],
            launched_at=launched_at,
            logo_url=data.get('logo_url')
        )

    @classmethod
    def from_hit(cls, hit: dict) -> 'Company':
        """
        Create a Company instance from an Algolia hit
        """
        return cls(
            id=hit['id'],
            name=hit['name'],
            slug=hit['slug'],
            website=hit['website'],
            description=hit['long_description'],
            one_liner=hit['one_liner'],
            batch=hit['batch'],
            status=hit['status'],
            team_size=hit['team_size'],
            industry=hit['industry'],
            subindustry=hit['subindustry'],
            industries=hit['industries'],
            regions=hit['regions'],
            locations=hit['all_locations'],
            tags=hit['tags'],
            stage=hit['stage'],
            is_hiring=hit['isHiring'],
            is_nonprofit=hit['nonprofit'],
            is_top_company=hit['top_company'],
            launched_at=datetime.fromtimestamp(hit['launched_at']) if hit.get('launched_at') else None,
            logo_url=hit.get('small_logo_thumb_url')
        ) 