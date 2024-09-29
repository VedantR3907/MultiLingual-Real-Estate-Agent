
from crewai import Agent, LLM, Crew, Task
from crewai_tools import TXTSearchTool
from dotenv import load_dotenv

load_dotenv()

tool = TXTSearchTool(
    txt='../Vedant Rajpurohit Resume new.txt',
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama3.1",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="ollama", # or openai, ollama, ...
            config=dict(
                model="llama3.1"
                # title="Embeddings",
            ),
        ),
    )
)

llm = LLM(
    model = 'ollama/llama3.1',
    base_url='http://localhost:11434',
    # api_key=os.environ.get("GROQ_API_KEY")
)

agent = Agent(
    role='Information provider of Documents',
    goal='Provide tailored responses and gets the relevant information from the document according to the user query: - {input}',
    backstory="An expert to search and find relevant information from the document provided.",
    llm=llm,
    tools=[tool],
    verbose=True,
)

task = Task(
    agent=agent,
    description='Your task is to filter and get the top information from the document according to the user query: - {input}. Never generate any response outside of the document. If you dont know the answer jsut say you dont know the answer never give wrong information to the user',
    expected_output='The output should be a single paragraph.',
    output_file='./output_crew_ai.txt'
)

my_crew = Crew(agents=[agent], tasks=[task])
crew = my_crew.kickoff(inputs={"input": "What is the name of research paper published by vedant. Also what is vedant's recent company he worked in."})

print(crew)