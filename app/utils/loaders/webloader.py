import asyncio
import re
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
    keywords = ["signup", "sign up", "sign in", "signin","login", "register", "join free", "facebook", "instagram", "twitter", "youtube", "click here", "sign in", "join free", "linkedin", 'whatsapp']
    
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

        # Save the cleaned content to a file
        with open('./cleaned_text.txt', 'w', encoding='utf8') as f:
            f.write(cleaned_content)

        print("Cleaned content saved to './cleaned_text.txt'")

# Run the async main function
# asyncio.run(WebLoader())
