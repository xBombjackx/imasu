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
            """
You are a creative assistant that generates images based on user prompts.

**Your primary task is to:**
1.  Analyze the user's input to understand the core creative idea.
2.  Refine and enhance the user's prompt to be more descriptive, vivid, and suitable for a text-to-image model. Add artistic details, lighting, and composition suggestions.
3.  Call the `generate_image` tool with the refined prompt.

**Output Format:**
- You **MUST** call the `generate_image` tool.
- Your final response should **ONLY** be the direct output from the tool call.
- Do **NOT** add any conversational text, markdown, or explanations.
""",
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

llm = ChatOllama(
    model=settings.OLLAMA_MODEL, temperature=0.7, base_url=settings.OLLAMA_URL
)

tools = get_tools()

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
