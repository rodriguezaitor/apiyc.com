"""
Example usage of the YC API client
"""

from datetime import timedelta
from apiyc import YCClient

def print_batch_stats(client: YCClient):
    """Print statistics about YC batches"""
    print("\nBatch Statistics:")
    
    # Get batch statistics
    stats = client.get_batch_statistics()
    
    # Print total numbers
    print(f"Total number of batches: {len(stats)}")
    print(f"Total number of companies across all batches: {sum(stats.values())}")
    
    # Print companies per batch
    print("\nCompanies per batch (sorted by count):")
    sorted_batches = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    for batch, count in sorted_batches:
        print(f"{batch}: {count} companies")

def print_company_stats(client: YCClient):
    """Print general statistics about YC companies"""
    print("\nCompany Statistics:")
    
    stats = client.get_company_stats()
    print(f"Total companies: {stats['total_companies']}")
    print(f"Companies currently hiring: {stats['hiring']}")
    print(f"Top companies: {stats['top_companies']}")
    print(f"Nonprofit companies: {stats['nonprofit']}")

def print_batch_companies(client: YCClient, batch: str, use_cache: bool = True):
    """Print details about companies in a specific batch"""
    print(f"\nCompanies in batch {batch} (use_cache={use_cache}):")
    
    companies = client.get_companies_by_batch(batch, use_cache=use_cache)
    print(f"Total number of companies found: {len(companies)}")
    
    for company in companies:
        print(f"- {company.name}: {company.one_liner}")

def print_facet_data(client: YCClient, use_cache: bool = True):
    """Print various facet data"""
    print(f"\nFetching facet data (use_cache={use_cache}):")
    
    # Print region statistics
    print("\nRegion Statistics:")
    regions = client.get_facet_data("regions", use_cache=use_cache)
    sorted_regions = sorted(regions.items(), key=lambda x: x[1], reverse=True)
    for region, count in sorted_regions:
        print(f"{region}: {count} companies")
    
    # Print industry statistics
    print("\nIndustry Statistics:")
    industries = client.get_facet_data("industries", use_cache=use_cache)
    sorted_industries = sorted(industries.items(), key=lambda x: x[1], reverse=True)
    for industry, count in sorted_industries:
        print(f"{industry}: {count} companies")
    
    # Print subindustry statistics
    print("\nSubindustry Statistics:")
    subindustries = client.get_facet_data("subindustry", use_cache=use_cache)
    sorted_subindustries = sorted(subindustries.items(), key=lambda x: x[1], reverse=True)[:10]  # Top 10
    print("Top 10 subindustries:")
    for subindustry, count in sorted_subindustries:
        print(f"{subindustry}: {count} companies")

def print_all_data(client: YCClient):
    """Print all companies and facets data"""
    print("\nFetching all YC data...")
    companies, facets = client.get_all_data(use_cache=True)
    
    # Print company statistics
    print(f"\nTotal companies fetched: {len(companies)}")
    print("\nCompanies by status:")
    status_counts = {}
    for company in companies:
        status_counts[company.status] = status_counts.get(company.status, 0) + 1
    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{status}: {count} companies")
    
    # Print facet statistics
    print("\nFacet Statistics:")
    for facet_type, facet_data in facets.items():
        print(f"\n{facet_type.title()} (top 5):")
        sorted_data = sorted(facet_data.items(), key=lambda x: x[1], reverse=True)[:5]
        for value, count in sorted_data:
            print(f"{value}: {count}")

def demonstrate_caching():
    """Demonstrate the facet and company data caching functionality"""
    client = YCClient()
    
    print("\nStep 1: Fetching and saving all facets...")
    client.fetch_and_save_all_facets()
    
    print("\nStep 2: Getting facet data from cache...")
    print_facet_data(client, use_cache=True)
    
    print("\nStep 3: Fetching and caching W25 companies...")
    print_batch_companies(client, "W25", use_cache=False)
    
    print("\nStep 4: Getting W25 companies from cache...")
    print_batch_companies(client, "W25", use_cache=True)
    
    print("\nStep 5: Force refreshing W25 companies...")
    client.refresh_companies("W25")
    
    print("\nStep 6: Getting W25 companies with a short cache timeout...")
    companies = client.get_companies_by_batch("W25", max_age=timedelta(minutes=5))
    print(f"Number of companies in W25: {len(companies)}")

def main():
    """Main function"""
    client = YCClient()
    
    # Print all data
    print_all_data(client)
    
    # Print batch statistics
    print_batch_stats(client)
    
    # Print company statistics
    print_company_stats(client)

if __name__ == "__main__":
    main() 