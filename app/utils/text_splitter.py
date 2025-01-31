import re
import os
import json
import aiofiles
import asyncio
import sys
sys.path.append('../')
from typing import Dict, Any
from datetime import datetime
from langchain.text_splitter import MarkdownTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.constants.constants import FILES_OUTPUT_DIR

def filter_filename(filename: str, id: bool) -> str:
    """
    Filter and format the filename based on the given parameters.

    Args:
        filename (str): The original filename.
        id (bool): If True, keep the '.' and '#' characters; otherwise, remove them.

    Returns:
        str: The filtered and formatted filename.
    """
    # Split the filename into name and extension
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')

    # Handle the case where there's no extension
    if ext:
        ext = '.' + ext
    
    # Remove special characters and spaces, keeping '.' and '#' if id is True
    if not id:
        name = re.sub(r'[^\w\s#.]', '', name)
    else:
        name = re.sub(r'[^\w\s.#]', '', name)

    # Remove spaces and capitalize the first letter of each word
    name = re.sub(r'\s+', '', name.title())

    # Reassemble the filename
    filtered_filename = name + ext
    
    return filtered_filename

async def ReadFiles(folder_path: str) -> Dict[str, Dict[str, str]]:
    """
    Reads all text files in the specified folder and returns their contents along with metadata.

    Args:
        folder_path (str): The path to the folder containing text files.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary where keys are file names and values are dictionaries containing:
            - 'content': The file content as a string.
            - 'creation_date': The file creation date as a string in 'YYYY-MM-DD' format.
            - 'last_modified_date': The file last modified date as a string in 'YYYY-MM-DD' format.
            - 'file_path': The full path to the file.
            - 'file_size': The file size in bytes.
    """
    file_contents = {}
    for filename in os.listdir(folder_path):
        file_path_full = os.path.join(folder_path, filename)
        if os.path.isfile(file_path_full) and filename.endswith('.txt'):
            creation_date = datetime.fromtimestamp(os.path.getctime(file_path_full)).strftime('%Y-%m-%d')
            last_modified_date = datetime.fromtimestamp(os.path.getmtime(file_path_full)).strftime('%Y-%m-%d')
            file_size = os.path.getsize(file_path_full)
            
            async with aiofiles.open(file_path_full, 'r', encoding='utf-8') as file:
                content = await file.read()
                
            file_contents[filename] = {
                'content': content,
                'creation_date': creation_date,
                'last_modified_date': last_modified_date,
                'file_path': file_path_full,
                'file_size': file_size
            }
    return file_contents

async def TextSplitter(file_contents: Dict[str, Dict[str, str]], file_type: str) -> Dict[str, Dict[str, str]]:
    """
    Splits the text content of each file into smaller chunks using MarkdownTextSplitter.

    Args:
        file_contents (Dict[str, Dict[str, str]]): A dictionary where keys are file names and values are dictionaries containing:
            - 'content': The file content as a string.
            - 'creation_date': The file creation date as a string.
            - 'last_modified_date': The file last modified date as a string.
            - 'file_path': The full path to the file.
            - 'file_size': The file size in bytes.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary where keys are chunk IDs and values are dictionaries containing:
            - 'ID': The chunk ID.
            - 'text': The split text chunk.
            - 'creation_date': The file creation date.
            - 'file_name': The file name.
            - 'file_path': The file path.
            - 'file_size': The file size.
            - 'last_modified_date': The file last modified date.
    """
    metadata = {}
    # Initialize the MarkdownTextSplitter with the desired chunk size and overlap
    if file_type == 'weblinks':
        splitter = MarkdownTextSplitter(chunk_size=1500, chunk_overlap=150)
    else:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    
    for file_name, file_metadata in file_contents.items():
        content = file_metadata['content']
        # Create documents using the MarkdownTextSplitter
        docs = splitter.create_documents([content])
        
        for i, doc in enumerate(docs):
            chunk_id = f"{file_name}#chunk_{i}"
            metadata[chunk_id] = {
                'ID': chunk_id,
                'text': doc.page_content,
                'creation_date': file_metadata['creation_date'],
                'file_name': os.path.basename(file_metadata['file_path']),
                'file_path': file_metadata['file_path'],
                'file_size': file_metadata['file_size'],
                'last_modified_date': file_metadata['last_modified_date']
            }
    
    return metadata

async def WriteMetadataToJson(metadata: Dict[str, Dict[str, Any]], output_path: str) -> None:
    """
    Writes the metadata to a JSON file with a new structure.

    Args:
        metadata (Dict[str, Dict[str, Any]]): The metadata dictionary to be written to the JSON file.
        output_path (str): The path where the JSON file will be saved.
    """
    # Reformat the metadata to the new structure
    reformatted_data = []
    for chunk_id, chunk_metadata in metadata.items():
        reformatted_data.append({
            "id": filter_filename(chunk_id, id=True),
            "values": chunk_metadata.get('embedding', []),  # Include embeddings if available
            "metadata": {
                "text": chunk_metadata['text'],  # Include the text content in the metadata
                "creation_date": chunk_metadata['creation_date'],
                "file_name": chunk_metadata['file_name'],
                "file_path": chunk_metadata['file_path'],
                "file_size": chunk_metadata['file_size'],
                "last_modified_date": chunk_metadata['last_modified_date']
            }
        })
    
    # Write the reformatted data to the JSON file
    async with aiofiles.open(output_path, 'w', encoding='utf-8') as json_file:
        await json_file.write(json.dumps(reformatted_data, ensure_ascii=False, indent=4))

async def process_metadata(directory_path: str, file_type: str) -> None:
    """
    Processes files in the specified directory to create metadata and write it to a JSON file.

    Args:
        directory_path (str): The path to the directory containing files to process.
    """
    # Construct the path to the extracted_output folder in the specified base path
    extracted_output_path = directory_path

    # Ensure that the path exists and is a directory
    if os.path.isdir(extracted_output_path):
        if file_type == 'weblinks':
            documents_dir = os.path.join(extracted_output_path, 'weblink-documents')
        else:
            documents_dir = os.path.join(extracted_output_path, 'pdf-documents')
        print(f"Processing files in the directory: {documents_dir}")
        
        # Read all files in the extracted_output folder
        file_contents = await ReadFiles(documents_dir)

        # Split the text and create metadata using MarkdownTextSplitter
        metadata = await TextSplitter(file_contents, file_type)

        # Define the path for the JSON output file
        json_output_path = os.path.join(extracted_output_path, 'metadata.json')

        # Write the metadata to the JSON file
        await WriteMetadataToJson(metadata, json_output_path)

        print(f"Metadata has been written to {json_output_path}.")
    else:
        print(f"The path {extracted_output_path} is not a valid directory.")
    
if __name__ == "__main__":
    # Run the async process_metadata function
    asyncio.run(process_metadata(FILES_OUTPUT_DIR, 'weblinks'))
