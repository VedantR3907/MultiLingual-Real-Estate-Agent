import os
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from llama_index.llms.groq import Groq
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

load_dotenv()

PINECONE_CLIENT = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
PINECONE_INDEX_NAME = 'realestatebot'
PINECONE_NAMESPACE_DOCUMENTS = 'docs-weblinks'
GROQ_CLIENT_LLAMAINDEX = Groq(model="llama3-70b-8192", api_key=os.environ.get("GROQ_API_KEY"),)
EMBEDDING_MODEL = FastEmbedEmbeddings()

SIMILARITY_TOP_K = 10
SIMILARITY_CUTOFF = 0.0

current_dir = os.path.dirname(os.path.abspath(__file__))
DIRECTORY_PATH = os.path.dirname(os.path.dirname(current_dir))

FILES_INPUT_DIR = fr'{DIRECTORY_PATH}\db\documents'
FILES_OUTPUT_DIR = fr'{DIRECTORY_PATH}\db\extracted_output'




FASTAPI_URL = "http://127.0.0.1:8000"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = 'gemini-1.5-flash'