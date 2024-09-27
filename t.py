import os
from langchain.text_splitter import MarkdownTextSplitter

# Define the input file path and output folder
input_file = './app/db/extracted_output/3bkh-flats-apartments-for-sale-in-bhankrota-jaipur-1800-sq-ft-57-60-lac-1079848.txt'
output_folder = './output_text/'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read the input markdown text
with open(input_file, 'r') as f:
    markdown_text = f.read()

# Initialize the MarkdownTextSplitter with the desired chunk size and overlap
markdown_splitter = MarkdownTextSplitter(chunk_size=1500, chunk_overlap=100)
docs = markdown_splitter.create_documents([markdown_text])

# Save each chunk in a separate file with numbering
for idx, doc in enumerate(docs):
    output_file = os.path.join(output_folder, f'chunk_{idx + 1}.txt')
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(doc.page_content)
    print(f"Chunk {idx + 1} saved as {output_file}")
