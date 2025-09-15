from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.agent import agent_executor, MEMORY

router = APIRouter()

class GenerationRequest(BaseModel):
    prompt: str

@router.get("/")
def read_root():
    return {"message": "Welcome to the Agentic API"}

@router.post("/agent/generate")
async def agent_generate(request: GenerationRequest):
    """
    Accepts a prompt and uses the LangChain agent to generate a response,
    which may include generating an image. It now maintains conversational memory.
    """
    print(f"--- Calling Agent with prompt: '{request.prompt}' ---")

    # Load the history from our memory object
    chat_history = MEMORY.load_memory_variables({})["chat_history"]

    response = await agent_executor.ainvoke(
        {
            "input": request.prompt,
            "chat_history": chat_history,
        }
    )

    # Save the new interaction into memory
    MEMORY.save_context(
        {"input": request.prompt},
        {"output": response["output"]},
    )

    return {"response": response}
