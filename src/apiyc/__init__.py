"""
API YC - Y Combinator Companies API Client
"""

__version__ = "0.1.0"

from .clients.yc import YCClient
from .clients.algolia import AlgoliaClient
from .types.algolia import AlgoliaResponse, CompanyHit
from .types.company import Company

__all__ = [
    "YCClient",
    "AlgoliaClient",
    "AlgoliaResponse",
    "CompanyHit",
    "Company"
] 