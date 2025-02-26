"""
Script to update README with last update timestamp
"""
import re
from datetime import datetime
from pathlib import Path

def update_readme_timestamp() -> None:
    """Update the README.md file with the current timestamp"""
    readme_path = Path("README.md")
    timestamp_file = Path("data/last_update.txt")
    
    # Read current timestamp
    if not timestamp_file.exists():
        return
        
    timestamp = datetime.fromisoformat(timestamp_file.read_text().strip())
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Read README content
    content = readme_path.read_text()
    
    # Update or add timestamp section
    timestamp_section = f"\n## Last Updated\n\nData last updated at: {timestamp_str}\n"
    
    if "## Last Updated" in content:
        # Update existing timestamp
        content = re.sub(
            r"## Last Updated\n\nData last updated at:.*?\n",
            timestamp_section,
            content,
            flags=re.DOTALL
        )
    else:
        # Add timestamp section before License
        if "## License" in content:
            content = content.replace("## License", f"{timestamp_section}\n## License")
        else:
            content += f"\n{timestamp_section}"
    
    # Write updated content
    readme_path.write_text(content)

if __name__ == "__main__":
    update_readme_timestamp() 