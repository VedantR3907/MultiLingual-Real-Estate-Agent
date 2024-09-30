import sys
from typing import List
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import Settings, VectorStoreIndex, get_response_synthesizer  # noqa: F401
from llama_index.core.chat_engine.context import ContextChatEngine
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.postprocessor import LongContextReorder
from llama_index.core.retrievers import VectorIndexRetriever
sys.path.append('../')
from utils.constants.constants import (GROQ_CLIENT_LLAMAINDEX, 
                       PINECONE_CLIENT, PINECONE_INDEX_NAME, PINECONE_NAMESPACE_DOCUMENTS, 
                       SIMILARITY_TOP_K)
from utils.prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

Settings.embed_model=embed_model
Settings.llm = GROQ_CLIENT_LLAMAINDEX
# Settings.llm = Gemini(api_key=os.environ.get("GEMINI_API_KEY"), model ='models/gemini-1.5-flash')

def pinecone_vectorstore():
    index = PINECONE_CLIENT.Index(PINECONE_INDEX_NAME)
    pinecone_vector_store = PineconeVectorStore(pinecone_index=index, namespace=PINECONE_NAMESPACE_DOCUMENTS)

    return VectorStoreIndex.from_vector_store(vector_store=pinecone_vector_store)


async def llamaindex_chatbot(query: str, chat_history: List):
    vector_index_retriever = VectorIndexRetriever(
    index=pinecone_vectorstore(),
    namespace=PINECONE_NAMESPACE_DOCUMENTS,
    similarity_top_k=SIMILARITY_TOP_K)
    reorder = LongContextReorder()
    postprocessors = [reorder]

    chatengine = ContextChatEngine(
            retriever=vector_index_retriever,
            node_postprocessors=postprocessors,
            prefix_messages = [ChatMessage(role="system", content=SYSTEM_PROMPT

    )],
            llm = Settings.llm,
            memory=ChatMemoryBuffer.from_defaults(chat_history = chat_history, token_limit=5000))
    
    chat_response = await chatengine.achat(query)

    return str(chat_response)

if __name__ == "__main__":
    llamaindex_chatbot("Are there any properties between 50 to 60 lakhs", [])
