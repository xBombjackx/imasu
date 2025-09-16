import base64
import json
import requests
from langchain.tools import tool
from pathlib import Path
import time
from typing import Optional

from pydantic import BaseModel, Field

from app.core.settings import settings


# --- Pydantic Model for Tool Input ---
# This model defines the "contract" for the image generation tool.
# By using a Pydantic model, we allow the LLM to provide a richer set of
# parameters, but we validate them strictly. The LLM can be "creative,"
# and we can handle it gracefully.
class ImageGeneratorInput(BaseModel):
    prompt: str = Field(description="A detailed, descriptive prompt for the image.")
    negative_prompt: Optional[str] = Field(
        default="ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face",
        description="A detailed prompt of things to exclude from the image.",
    )
    steps: Optional[int] = Field(
        default=None, description="Number of sampling steps (e.g., 20-40)."
    )
    cfg_scale: Optional[float] = Field(
        default=7.0, description="Classifier-Free Guidance scale (e.g., 7.0)."
    )
    width: Optional[int] = Field(default=None, description="Image width in pixels.")
    height: Optional[int] = Field(default=None, description="Image height in pixels.")
    sampler_name: Optional[str] = Field(
        default=None, description="The sampling method (e.g., 'Euler', 'DPM++ 2M Karras')."
    )


# --- Tool Definition ---
# We now pass the Pydantic model directly to the @tool decorator.
# LangChain will automatically handle the conversion from the LLM's JSON output
# into a populated instance of the ImageGeneratorInput class.
@tool(args_schema=ImageGeneratorInput)
def generate_image(tool_input: ImageGeneratorInput) -> str:
    """
    Generates an image from a text prompt and other parameters using the AUTOMATIC1111 API.
    Returns a JSON string containing the image data and final prompt.
    """
    print("--- 🖼️ Calling Image Generation Tool with Pydantic Model ---")
    print(f"Tool Input: {tool_input.model_dump_json(indent=2)}")

    # --- Set Image Quality Defaults based on FAST_MODE ---
    # If the user (or LLM) provides specific values, they will override these.
    if settings.FAST_MODE:
        default_steps = 10
        default_sampler = "Euler"
        default_width = 512
        default_height = 512
    else:
        default_steps = 25
        default_sampler = "DPM++ 2M Karras"
        default_width = 1024
        default_height = 1024

    # --- API Payload ---
    # We construct the payload by coalescing the validated tool input with our defaults.
    # This is the core of the robust solution: we trust our Pydantic model, not the raw LLM output.
    payload = {
        "prompt": tool_input.prompt,
        "negative_prompt": tool_input.negative_prompt,
        "steps": tool_input.steps or default_steps,
        "cfg_scale": tool_input.cfg_scale,
        "width": tool_input.width or default_width,
        "height": tool_input.height or default_height,
        "sampler_name": tool_input.sampler_name or default_sampler,
    }

    # --- Make the API Request ---
    try:
        response = requests.post(
            url=f"{settings.A1111_URL}/sdapi/v1/txt2img", json=payload, timeout=180
        )
        response.raise_for_status()
        r = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling A1111 API: {e}")
        error_result = {"error": "Failed to connect to the image generation server."}
        return json.dumps(error_result)

    if "images" in r and r["images"]:
        # --- Decode and Save the Image ---
        image_data = r["images"][0]
        image_bytes = base64.b64decode(image_data)

        output_path = Path(settings.OUTPUT_DIR)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = int(time.time())
        file_path = output_path / f"generated_image_{timestamp}.png"

        with open(file_path, "wb") as f:
            f.write(image_bytes)
        print(f"Image saved to: {file_path}")

        # --- Prepare the JSON Output ---
        # The final prompt used is now part of the payload.
        result = {
            "image_base64": image_data,
            "final_prompt": payload["prompt"],
            "saved_path": str(file_path),
        }
        return json.dumps(result)
    else:
        print("API response did not contain image data.")
        error_result = {"error": "The image generation server did not return an image."}
        return json.dumps(error_result)
