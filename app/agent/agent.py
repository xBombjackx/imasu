# app/agent/agent.py
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_openai_functions_agent

from app.core.settings import settings
from .tools import generate_image

# --- 1. Define the Tools ---
tools = [generate_image]

# --- 2. Create the LLM ---
llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    temperature=0.7,
    format="json",
    base_url=settings.OLLAMA_URL,  # <-- ADD THIS PARAMETER
)
# --- 3. Create the Prompt ---
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant whose only purpose is to call the 'generate_image' tool. "
            "The 'generate_image' tool takes a single string argument named 'prompt'. "
            "Your sole output must be a JSON object that calls the 'generate_image' tool with this single 'prompt' argument.",
        ),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# --- 4. Create the Agent ---
agent = create_openai_functions_agent(llm, tools, prompt)


# --- 5. Create the Agent Executor ---
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
