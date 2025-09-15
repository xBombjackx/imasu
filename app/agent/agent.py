from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from app.agent.tools import generate_image

# 1. Initialize the LLM
llm = ChatOllama(model="llama3.1:8b", temperature=0)

# 2. Define the list of tools the agent can use
tools = [generate_image]

# 3. Create the Agent Prompt Template
# We are adapting the original custom prompt to work with the ReAct agent.
# The key is to ensure the prompt template can accept 'tools' and 'tool_names'
# and that the system message includes instructions on how to use them.
# The `render_text_description` function (default in create_react_agent)
# will format the tools list into a string that fills the {tools} placeholder.

system_prompt_template = """
You are a creative assistant who helps users generate images.
If the user's request is ambiguous, ask for clarification.
When you generate an image, enhance the user's prompt to be more descriptive and artistic for the image model.
Always confirm when an image has been successfully created.

You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_template),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)


# 4. Create the Agent
agent = create_react_agent(llm, tools, prompt)

# 5. Create the Agent Executor
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# 6. Create a memory object
MEMORY = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
