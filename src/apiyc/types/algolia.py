"""
Algolia API response types
"""

from typing import TypedDict, Dict, List, Optional, Any, Literal

# Define all possible facet types
FacetType = Literal[
    "batch",
    "regions",
    "isHiring",
    "nonprofit",
    "industries",
    "app_answers",
    "subindustry",
    "top_company",
    "app_video_public",
    "question_answers",
    "demo_day_video_public"
]

class HighlightResultValue(TypedDict):
    value: str
    matchLevel: str
    matchedWords: List[str]

class HighlightResultTag(TypedDict):
    value: str
    matchLevel: str
    matchedWords: List[str]

class HighlightResult(TypedDict):
    name: HighlightResultValue
    website: HighlightResultValue
    all_locations: HighlightResultValue
    long_description: HighlightResultValue
    one_liner: HighlightResultValue
    tags: List[HighlightResultTag]

class CompanyHit(TypedDict):
    id: int
    name: str
    slug: str
    former_names: List[str]
    small_logo_thumb_url: str
    website: str
    all_locations: str
    long_description: str
    one_liner: str
    team_size: int
    industry: str
    subindustry: str
    launched_at: int
    tags: List[str]
    tags_highlighted: List[str]
    top_company: bool
    isHiring: bool
    nonprofit: bool
    batch: str
    status: str
    industries: List[str]
    regions: List[str]
    stage: str
    app_video_public: bool
    demo_day_video_public: bool
    app_answers: Optional[bool]
    question_answers: bool
    objectID: str
    _highlightResult: HighlightResult

class ProcessingTimingsMS(TypedDict):
    _request: Dict[str, int]
    extensions: int
    total: int

class ExhaustiveInfo(TypedDict):
    facetsCount: bool
    nbHits: bool
    typo: bool

class Extensions(TypedDict):
    queryCategorization: Dict[str, Any]

class FacetCounts(TypedDict):
    batch: Dict[str, int]
    regions: Dict[str, int]
    isHiring: Dict[str, int]
    nonprofit: Dict[str, int]
    industries: Dict[str, int]
    app_answers: Dict[str, int]
    subindustry: Dict[str, int]
    top_company: Dict[str, int]
    app_video_public: Dict[str, int]
    question_answers: Dict[str, int]
    demo_day_video_public: Dict[str, int]

class AlgoliaResult(TypedDict):
    hits: List[CompanyHit]
    nbHits: int
    page: int
    nbPages: int
    hitsPerPage: int
    facets: FacetCounts
    exhaustiveFacetsCount: bool
    exhaustiveNbHits: bool
    exhaustiveTypo: bool
    exhaustive: ExhaustiveInfo
    query: str
    params: str
    index: str
    renderingContent: Dict[str, Any]
    extensions: Extensions
    processingTimeMS: int
    processingTimingsMS: ProcessingTimingsMS
    serverTimeMS: int

class AlgoliaResponse(TypedDict):
    results: List[AlgoliaResult] 