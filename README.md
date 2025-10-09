# Y Combinator Companies API Client

A Python client for accessing Y Combinator companies data through their Algolia API.

## Features

- Fetch companies by batch
- Get batch statistics
- Get company statistics
- Type-safe responses
- Clean, object-oriented interface
- Intelligent caching system for both facets and companies
- Configurable cache timeouts
- Batch-specific data storage
- Automated data updates every 6 hours

## Installation

```bash
pip install -e .
```

## Usage

### Basic Usage

```python
from apiyc import YCClient

# Create a client
client = YCClient()

# Get companies from a specific batch
companies = client.get_companies_by_batch("W25")
for company in companies:
    print(f"{company.name}: {company.one_liner}")

# Get batch statistics
stats = client.get_batch_statistics()
print(f"Total batches: {len(stats)}")
print(f"Total companies: {sum(stats.values())}")

# Get company statistics
company_stats = client.get_company_stats()
print(f"Companies hiring: {company_stats['hiring']}")
print(f"Top companies: {company_stats['top_companies']}")
```

### Caching Features

```python
from datetime import timedelta
from apiyc import YCClient

client = YCClient()

# Use cached data with default timeout (24 hours)
companies = client.get_companies_by_batch("W25", use_cache=True)

# Use cached data with custom timeout
companies = client.get_companies_by_batch("W25", max_age=timedelta(hours=1))

# Force refresh cache for a batch
companies = client.refresh_companies("W25")

# Get facet data with caching
regions = client.get_facet_data("regions", use_cache=True)

# Force refresh facet data
client.refresh_facet_data("regions")

# Fetch and cache all facets
client.fetch_and_save_all_facets()

# Get all companies and facets
companies, facets = client.get_all_data()
```

### Data Storage Structure

The client maintains a structured cache in the following directories:

```
data/
├── companies/
│   ├── W25.json
│   ├── W24.json
│   └── ...
├── facets/
│   ├── batch.json
│   ├── regions.json
│   ├── industries.json
│   └── ...
└── metadata.json
```

Each cached file includes:

- The actual data
- Timestamp of when it was fetched
- Version information (in metadata.json)

## Project Structure

```
src/
├── apiyc/
│   ├── __init__.py
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── algolia.py
│   │   └── yc.py
│   ├── types/
│   │   ├── __init__.py
│   │   ├── algolia.py
│   │   └── company.py
│   └── utils/
│       ├── __init__.py
│       └── data_manager.py
├── main.py
└── setup.py
```

## Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install in development mode: `pip install -e .`

## Cache Management

The caching system is designed to:

- Store each batch's companies in separate files for efficient access
- Maintain timestamps for intelligent cache invalidation
- Support configurable timeouts per operation
- Allow forced refresh of specific data
- Handle JSON serialization of complex types (e.g., datetime)
- Automatically update every 6 hours via GitHub Actions





































































































































































































































































































































































































































































































































































































































































































































































































































































































































## Last Updated

Data last updated at: 2025-10-09 06:01:19 UTC

## License

MIT License
