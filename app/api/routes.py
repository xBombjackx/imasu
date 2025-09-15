from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.agent import agent_executor, MEMORY
import json  # <-- Add this import
import re  # <-- Add this import

router = APIRouter()


class GenerationRequest(BaseModel):
    prompt: str


# Define a Pydantic model for a structured response
class AgentResponse(BaseModel):
    output: str
    image_filename: str | None = None


@router.post(
    "/agent/generate", response_model={"response": AgentResponse}
)  # <-- Update response model hint
async def agent_generate(request: GenerationRequest):
    """
    Accepts a prompt and uses the LangChain agent to generate a response,
    which may include generating an image. It now maintains conversational memory.
    """
    print(f"--- Calling Agent with prompt: '{request.prompt}' ---")

    chat_history = MEMORY.load_memory_variables({})["chat_history"]

    response = await agent_executor.ainvoke(
        {
            "input": request.prompt,
            "chat_history": chat_history,
        }
    )

    MEMORY.save_context(
        {"input": request.prompt},
        {"output": response["output"]},
    )

    # Parse the agent's output to find the filename
    output_text = response.get("output", "")
    image_filename = None

    # Try to parse the output as JSON, which our tool now returns
    try:
        # The tool's JSON output might be embedded in the agent's final answer string.
        # We use a regex to find the JSON blob.
        json_match = re.search(r"\{.*\}", output_text)
        if json_match:
            tool_output = json.loads(json_match.group())
            image_filename = tool_output.get("image_filename")
            # We can also make the final text response cleaner
            output_text = tool_output.get("message", output_text)

    except (json.JSONDecodeError, TypeError):
        # If parsing fails, just return the raw text and no filename
        print("Could not parse JSON from agent output.")
        pass

    return {
        "response": AgentResponse(output=output_text, image_filename=image_filename)
    }
