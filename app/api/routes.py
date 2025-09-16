from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agent.agent import agent_executor, MEMORY
import traceback

router = APIRouter()


class GenerationRequest(BaseModel):
    prompt: str


class AgentResponse(BaseModel):
    output: str


@router.post("/ping")
async def ping():
    """A simple endpoint to check if the API is running."""
    return {"status": "ok"}


@router.post(
    "/agent/generate",
    # The 'response_model' is often a simpler way to declare the primary success response.
    # Using 'responses' is great for documenting multiple possible outcomes (e.g., 200, 404, 500).
    response_model=AgentResponse,
    responses={
        200: {
            # 💡 CHANGE A: The key here must be "model", not "response".
            "model": AgentResponse,
            "description": "Successful response from the agent",
        },
        500: {"description": "Internal server error"},
    },
)
async def agent_generate(request: GenerationRequest):
    """Receives a prompt and uses the agent to generate a response."""
    try:
        # Invoke the agent executor
        response = await agent_executor.ainvoke(
            {"input": request.prompt, "chat_history": MEMORY.buffer_as_messages}
        )
        # Update memory with the current interaction
        MEMORY.save_context({"input": request.prompt}, {"output": response["output"]})

        result = response["output"]

        # 💡 CHANGE B: Return a Pydantic model instance, not a dictionary.
        return AgentResponse(output=result)

    except Exception as e:
        # It's good practice to log the error here
        # import logging
        # logging.error(f"Error in agent generation: {e}")
        print(f"--- AN ERROR OCCURRED IN agent_generate ---")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
