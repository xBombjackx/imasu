import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

from app.agent.agent import agent_executor
from app.agent.ideation import ideation_chain

# --- Router and Logger Setup ---
router = APIRouter()
logger = logging.getLogger(__name__)


# --- Pydantic Models ---
class GenerationRequest(BaseModel):
    prompt: str


class AgentResponse(BaseModel):
    output: str
    image_base64: Optional[str] = None
    final_prompt: Optional[str] = None


# --- API Endpoints ---
@router.get("/ping")
def ping():
    """A simple ping endpoint to check if the server is running."""
    return {"status": "alive"}


@router.post("/agent/generate", response_model=AgentResponse)
async def agent_generate(request: GenerationRequest):
    """
    Receives a prompt, invokes the agent, and generates an image.
    The agent's output is expected to be a JSON string from the generate_image tool.
    This endpoint parses the JSON and returns a structured response.
    """
    try:
        # Invoke the agent. The agent's 'output' will be a JSON string from our tool.
        agent_response = await agent_executor.ainvoke({"input": request.prompt})

        # Extract the JSON string from the agent's output
        agent_output_str = agent_response.get("output")
        if not agent_output_str:
            raise HTTPException(
                status_code=500, detail="Agent failed to produce a valid output."
            )

        # Parse the JSON string to get the tool's results
        tool_result = json.loads(agent_output_str)

        # Construct a valid AgentResponse object for FastAPI to return to the UI
        api_response = AgentResponse(
            output=tool_result.get("final_prompt", "Image generated successfully."),
            image_base64=tool_result.get("image_base64"),
            final_prompt=tool_result.get("final_prompt"),
        )
        return api_response

    except json.JSONDecodeError as e:
        logger.exception(
            "JSONDecodeError: Agent returned malformed data. Details: %s", e
        )
        raise HTTPException(
            status_code=500,
            detail=f"Agent returned malformed data. Could not decode JSON from tool output: {agent_output_str}",
        )
    except Exception as e:
        logger.exception("An unexpected error occurred in /agent/generate: %s", e)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@router.post("/agent/variations")
async def agent_variations(request: GenerationRequest):
    """
    Receives a simple prompt and generates a list of creative variations using the ideation agent.
    """
    try:
        response = await ideation_chain.ainvoke({"user_idea": request.prompt})
        return response
    except Exception as e:
        logger.exception("An unexpected error occurred in /agent/variations: %s", e)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
