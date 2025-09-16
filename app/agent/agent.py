# app/agent/agent.py

from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_json_chat_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from .tools import generate_image

# --- CORE AGENT SETUP ---

# 1. Reasoning Engine (LLM)
llm = ChatOllama(model="llama3.1:8b", temperature=0.7)

# 2. Specialist Tools
tools = [generate_image]

# 3. Create a rigid, example-driven prompt to ensure correct JSON format.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI assistant that creates a prompt for an image generator.
Your response MUST be a single JSON blob containing "action" and "action_input" keys.
The "action_input" itself must contain "prompt" and "negative_prompt" keys.

You have access to the following tools: {tools}
You must use this tool: {tool_names}

- Based on the user's input, create a detailed, high-quality "prompt".
- Create a "negative_prompt" with terms like "deformed, blurry, bad anatomy, low quality".
- Do NOT add any text outside of the JSON blob.

This is the required format:
```json
{{
  "action": "generate_image",
  "action_input": {{
    "prompt": "A detailed, professional description of the image.",
    "negative_prompt": "A list of terms to avoid."
  }}
}}
```
            """,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# 4. Create the Agent
agent = create_json_chat_agent(llm, tools, prompt)

# 5. Create the Agent Executor with Memory
MEMORY = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=MEMORY,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
)

# --- INVOCATION FUNCTION ---


async def invoke_agent(prompt_text: str):
    """
    Asynchronously invokes the agent with a given prompt.
    """
    response = await agent_executor.ainvoke({"input": prompt_text})
    if "output" in response and response["output"]:
        return response["output"]
    elif "intermediate_steps" in response and response["intermediate_steps"]:
        return response["intermediate_steps"][0][1]
    return "Agent did not produce a final output or tool call."
