# app/agent/agent.py

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.agent.tools import get_tools
from app.core.settings import settings

# A more robust prompt that tells the LLM how to behave
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that is an expert at generating images.",
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = ChatOllama(
    model=settings.OLLAMA_MODEL, temperature=0, base_url=settings.OLLAMA_URL
)

tools = get_tools()

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
