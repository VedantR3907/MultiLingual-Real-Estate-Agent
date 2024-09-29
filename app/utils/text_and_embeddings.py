import os
import sys
import asyncio
sys.path.append('../')
from utils.text_splitter import process_metadata
from utils.generate_embeddings import generate_embeddings
from utils.constants.constants import FILES_OUTPUT_DIR

async def Generate_TextAndEmbeddings(directory_path: str, json_path: str, weblinks_or_document: str) -> None:
    # Process metadata
    await process_metadata(directory_path, weblinks_or_document)

    # Define the path to the metadata JSON file
    metadata_json_path = json_path

    # Generate embeddings and update the metadata
    await generate_embeddings(metadata_json_path)

    print(f"Metadata with embeddings has been updated in {metadata_json_path}.")

if __name__ == "__main__":
    # Define directory and JSON paths
    json_path = os.path.join(FILES_OUTPUT_DIR, 'metadata.json')

    # Run the async function
    asyncio.run(Generate_TextAndEmbeddings(FILES_OUTPUT_DIR, json_path, 'pdf'))