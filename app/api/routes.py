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


@router.post("/agent/generate", response_model=AgentGenerateResponse)
async def agent_generate(request: AgentGenerateRequest):
    """
    Generate an image using the agentic executor.
    """
    try:
        logger.info(f"Agent received prompt for generation: {request.prompt}")
        agent_response = await agent_executor.ainvoke({"input": request.prompt})

        # The new agent directly returns the tool's output!
        image_path = agent_response.get("output", "")
        if not image_path or not isinstance(image_path, str):
            raise HTTPException(
                status_code=500, detail="Agent did not return a valid image path."
            )

        logger.info(f"Agent generated image path: {image_path}")

        with open(image_path, "rb") as f:
            image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        return AgentGenerateResponse(image=image_base64)

    except Exception as e:
        logger.error(f"An unexpected error occurred in /agent/generate: {e}")
        # Re-raise as an HTTPException to send a 500 error to the client
        raise HTTPException(status_code=500, detail=str(e))

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
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


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
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
