import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
import base64

from app.agent.agent import agent_executor
from app.agent.ideation import ideation_chain

# --- Router and Logger Setup ---
router = APIRouter()
logger = logging.getLogger(__name__)


# --- Pydantic Models ---
class GenerationRequest(BaseModel):
    prompt: str


class AgentGenerateRequest(BaseModel):
    prompt: str


class AgentGenerateResponse(BaseModel):
    image_base64: str  # Rename 'image' to 'image_base64' to match the UI's expectation
    final_prompt: str  # Add the final prompt
    saved_path: str  # Add the path where the image was saved


class VariationsResponse(BaseModel):
    variations: List[str]


# --- API Endpoints ---
@router.get("/ping")
def ping():
    """A simple ping endpoint to check if the server is running."""
    return {"status": "alive"}


@router.post("/agent/generate", response_model=AgentGenerateResponse)
async def agent_generate(request: AgentGenerateRequest):
    """
    Generate an image using the agentic executor.
    """
    try:
        logger.info(f"Agent received prompt for generation: {request.prompt}")
        # The agent executor is now expected to return a JSON string from the tool
        agent_response_str = await agent_executor.ainvoke({"input": request.prompt})

        # The tool returns a JSON string, which is the output of the agent
        output_str = agent_response_str.get("output", "{}")
        tool_output = json.loads(output_str)

        image_base64 = tool_output.get("image_base64")

        if not image_base64:
            error_detail = tool_output.get(
                "error", "Agent did not return a valid image."
            )
            raise HTTPException(status_code=500, detail=error_detail)

        logger.info("Agent successfully generated image.")
        return AgentGenerateResponse(
            image_base64=tool_output.get("image_base64"),
            final_prompt=tool_output.get("final_prompt"),
            saved_path=tool_output.get("saved_path"),
        )

    except json.JSONDecodeError as e:
        logger.error(
            f"JSONDecodeError in /agent/generate: {e}. Raw output: {output_str}"
        )
        raise HTTPException(
            status_code=500,
            detail="Agent returned malformed data that could not be parsed as JSON.",
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred in /agent/generate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/variations", response_model=VariationsResponse)
async def agent_variations(request: GenerationRequest):
    """
    Receives a simple prompt and generates a list of creative variations using the ideation agent.
    """
    try:
        # The ideation chain already returns a dictionary thanks to the JsonOutputParser
        response_dict = await ideation_chain.ainvoke({"user_idea": request.prompt})
        return VariationsResponse(variations=response_dict.get("variations", []))
    except Exception as e:
        logger.exception("An unexpected error occurred in /agent/variations: %s", e)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
