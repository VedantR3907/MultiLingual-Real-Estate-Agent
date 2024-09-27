import os
import sys
import asyncio
sys.path.append('../../')
from utils.text_filtering.weblinks import process_metadata
from utils.embeddings.weblinks import generate_embeddings
from utils.constants.constants import FILES_OUTPUT_DIR

async def Generate_TextAndEmbeddings(directory_path: str, json_path: str) -> None:
    # Process metadata
    await process_metadata(directory_path)

    # Define the path to the metadata JSON file
    metadata_json_path = json_path

    # Generate embeddings and update the metadata
    await generate_embeddings(metadata_json_path)

    print(f"Metadata with embeddings has been updated in {metadata_json_path}.")

if __name__ == "__main__":
    # Define directory and JSON paths
    directory_path = os.path.join(FILES_OUTPUT_DIR, 'weblink-documents')
    json_path = os.path.join(FILES_OUTPUT_DIR, 'metadata.json')

    # Run the async function
    asyncio.run(Generate_TextAndEmbeddings(directory_path, json_path))
