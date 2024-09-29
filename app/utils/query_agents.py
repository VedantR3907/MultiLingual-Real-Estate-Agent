import os
import sys
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import Settings, VectorStoreIndex, get_response_synthesizer  # noqa: F401
from llama_index.core.llms import ChatMessage
from llama_index.core.postprocessor import LongContextReorder
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
sys.path.append('../')
from utils.constants.constants import (GROQ_CLIENT_LLAMAINDEX, 
                       PINECONE_CLIENT, PINECONE_INDEX_NAME, PINECONE_NAMESPACE_DOCUMENTS, )
from crewai import Agent, Task, Crew, LLM
from crewai_tools import LlamaIndexTool
from llama_index.core.llms import MessageRole
from llama_index.core import ChatPromptTemplate
load_dotenv()

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

llm = LLM(
    model = 'groq/llama-3.1-70b-versatile',
    api_key=os.environ.get("GROQ_API_KEY")
)

Settings.embed_model=embed_model
Settings.llm = GROQ_CLIENT_LLAMAINDEX
# Settings.llm = Gemini(api_key=os.environ.get("GEMINI_API_KEY"), model ='models/gemini-1.5-flash')

def pinecone_vectorstore():
    index = PINECONE_CLIENT.Index(PINECONE_INDEX_NAME)
    pinecone_vector_store = PineconeVectorStore(pinecone_index=index, namespace=PINECONE_NAMESPACE_DOCUMENTS)

    return VectorStoreIndex.from_vector_store(vector_store=pinecone_vector_store)


async def llamaindex_chatbot(query: str):
    vector_index_retriever = VectorIndexRetriever(
    index=pinecone_vectorstore(),
    namespace=PINECONE_NAMESPACE_DOCUMENTS,
    similarity_top_k=7)
    reorder = LongContextReorder()
    postprocessors = [reorder]
    chat_text_qa_msgs = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=(
                """ You are an assistant for answering real estate-related queries. Use the following pieces of retrieved information to answer questions about properties, such as available listings, property details (e.g., number of BHKs, facilities), and other relevant information. Provide clear and direct answers as if you're responding to a user's inquiry, without mentioning any documents or contexts. If you don't know the answer, just say that you don't know.

    You should always answer using the provided context and only the context from the document."""
            ),
        ),
        ChatMessage(
            role=MessageRole.USER,
            content=(
                "Context information is below.\n"
                "---------------------\n"
                "{context_str}\n"
                "---------------------\n"
                "Given the context information and not prior knowledge, "
                "answer the query.\n"
                "Query: {query_str}\n"
                "Answer: "
            ),
        ),
    ]
    text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

    response_synthesizer = get_response_synthesizer(response_mode='refine', text_qa_template=text_qa_template)
    postprocessors = [reorder]

    query_engine = RetrieverQueryEngine(
            retriever=vector_index_retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors = postprocessors
    )

    return query_engine

async def crewai_agent_chat(query):

    query_engine = await llamaindex_chatbot(query)

    query_tool = LlamaIndexTool.from_query_engine(
        query_engine,
        name="Real Estate Bot",
        description="This tool is a real estate chatbot that helps answer property-related queries, including available listings, BHK details, facilities, and other relevant real estate information using context from the retrieved documents."
    )

    # Define the Real Estate Researcher agent
    real_estate_agent = Agent(
        role="Real Estate Information Provider",
        goal="Provide tailored responses and retrieve relevant information from the document according to the user's query: {input}",
        backstory="""An expert in finding and filtering relevant information from the provided documents or databases.
        Your goal is to give concise and accurate information based on the user's query.""",
        llm=llm,
        tools=[query_tool],  # Pass the real estate bot query tool
        verbose=True,
    )

    # Define the task for the agent
    real_estate_task = Task(
        agent=real_estate_agent,
        description="""Your task is to filter and retrieve the most relevant information from the document based on the user's query: {input}.
        Never provide any information outside of the document. If you don't know the answer, simply say that you don't know. Never give incorrect information.""",
        expected_output="The output should be a single paragraph.",
        output_file='./output_crew_ai.txt'
    )

    # Create the Crew instance
    my_crew = Crew(agents=[real_estate_agent], tasks=[real_estate_task])

    crew = my_crew.kickoff(inputs={"input": query})

    print(crew.raw)

    return crew.raw