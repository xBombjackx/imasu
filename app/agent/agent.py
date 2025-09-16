from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_openai_functions_agent

from app.core.settings import settings
from .tools import generate_image

# --- 1. Define the Tools ---
tools = [generate_image]

# --- 2. Create the LLM ---
llm = ChatOllama(model=settings.OLLAMA_MODEL, temperature=0.7, format="json")

# --- 3. Create the Prompt ---
# With the Pydantic model handling validation, we can simplify the prompt.
# We no longer need to aggressively restrict the LLM. We can give it a more
# natural instruction, and LangChain will automatically provide the tool's
# schema (from the Pydantic model) to the LLM.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at generating images. "
            "Use the user's request to call the `generate_image` tool. "
            "If the user provides details like style, steps, or negative prompts, "
            "include them in the tool call.",
        ),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# --- 4. Create the Agent ---
agent = create_openai_functions_agent(llm, tools, prompt)


# --- 5. Create the Agent Executor ---
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
