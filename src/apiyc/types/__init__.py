"""
Type definitions for API responses and models
"""

from .algolia import (
    AlgoliaResponse,
    CompanyHit,
    FacetCounts,
    HighlightResult,
    HighlightResultValue,
    HighlightResultTag
)
from .company import Company

__all__ = [
    "AlgoliaResponse",
    "CompanyHit",
    "FacetCounts",
    "HighlightResult",
    "HighlightResultValue",
    "HighlightResultTag",
    "Company"
] 