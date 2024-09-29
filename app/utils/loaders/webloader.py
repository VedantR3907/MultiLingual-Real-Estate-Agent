import asyncio  # noqa: F401
import re
import os
import sys
sys.path.append('../../')
from utils.constants.constants import FILES_OUTPUT_DIR
from crawl4ai import AsyncWebCrawler

def clean_content(content):
    # Define the regex pattern to match unwanted image markdown
    patterns = [
        r'!\[.*?\]\(.*?\\\)\s*',  # Match any image markdown (with escaped quotes)
        r'!\[\\.*?\\\]\(.*?\\\)\s*',  # Match unwanted images with escaped quotes
        r'!\[\\\]\(.*?\\\)\s*',  # Match empty image markdown
        r'!\[.*?\]\(.*?\)\s*',  # Match standard image markdown (without escaped quotes)
    ]
    
    # Remove unwanted content
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)  # Remove all occurrences

    # Define keywords to filter out entire lines
    keywords = [
        "signup", "sign up", "sign in", "signin", "login", "register", 
        "join free", "facebook", "instagram", "twitter", "youtube", 
        "click here", "join free", "linkedin", "whatsapp"
    ]
    
    # Split the content into lines and filter out lines containing the keywords
    lines = content.splitlines()
    cleaned_lines = []
    
    for line in lines:
        # Check if any keyword is in the line (case-insensitive)
        if not any(keyword in line.lower() for keyword in keywords):
            cleaned_lines.append(line)
    
    # Join the cleaned lines back into a single string
    cleaned_content = '\n'.join(cleaned_lines).strip()  # Remove leading/trailing whitespace
    
    return cleaned_content

async def WebLoader(url):
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=url)

        # Extracted content in markdown format
        raw_content = result.markdown
        
        # Clean the extracted content
        cleaned_content = clean_content(raw_content)

        # Extract the base name from the URL
        base_name = os.path.basename(url)  # Get the last part of the URL
        file_name = base_name.split('.')[0]  # Remove the extension

        # Create the full output path
        output_path = os.path.join(FILES_OUTPUT_DIR + '\weblink-documents', f"{file_name}.txt")

        # Save the cleaned content to a file
        with open(output_path, 'w', encoding='utf8') as f:
            f.write(cleaned_content)

        print(f"Cleaned content saved to '{output_path}'")

# Example usage
url = "https://www.realestateindia.com/property-detail/3bkh-flats-apartments-for-sale-in-bhankrota-jaipur-1800-sq-ft-57-60-lac-1079848.htm"
asyncio.run(WebLoader(url))
