"""
Script to update all cached data
"""
import logging
from datetime import datetime
from pathlib import Path
from apiyc import YCClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def update_timestamp(timestamp: datetime) -> None:
    """
    Update the last update timestamp file
    
    Args:
        timestamp: Current update timestamp
    """
    timestamp_file = Path("data/last_update.txt")
    timestamp_file.write_text(timestamp.isoformat())

def validate_data(companies_count: int, facets_count: int) -> bool:
    """
    Validate the fetched data
    
    Args:
        companies_count: Number of companies fetched
        facets_count: Number of facet types fetched
        
    Returns:
        True if data is valid, False otherwise
    """
    if companies_count < 1000:  # YC should always have >1000 companies
        logger.error(f"Too few companies: {companies_count}")
        return False
        
    if facets_count < 5:  # We expect at least basic facets
        logger.error(f"Too few facet types: {facets_count}")
        return False
    
    return True

def main() -> None:
    """Update all cached data"""
    try:
        logger.info("Starting cache update")
        
        # Initialize client
        client = YCClient()
        
        # Update all data
        logger.info("Fetching all YC data...")
        companies, facets = client.get_all_data(use_cache=False)
        
        # Validate data
        if not validate_data(len(companies), len(facets)):
            raise ValueError("Data validation failed")
        
        # Log statistics
        logger.info(f"Updated data for {len(companies)} companies")
        logger.info(f"Updated {len(facets)} facet types")
        
        # Save timestamp
        now = datetime.now()
        update_timestamp(now)
        
        logger.info("Cache update completed successfully")
        
    except Exception as e:
        logger.error(f"Error updating cache: {e}")
        raise

if __name__ == "__main__":
    main() 