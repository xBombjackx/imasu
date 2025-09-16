import base64
import json
import requests
from langchain.tools import tool
from pathlib import Path
import time

from app.core.settings import settings


# --- Tool Definition ---
# By simplifying the tool definition to a standard function with a type-hinted
# string argument, we create a much clearer "contract" for the LLM.
# It no longer needs to guess the structure of a complex input object.
@tool
def generate_image(prompt: str) -> str:
    """
    Generates an image from a text prompt using the AUTOMATIC1111 API
    and returns a JSON string containing the image data and the final prompt.
    """
    print("--- 🖼️ Calling Image Generation Tool ---")
    print(f"Initial Prompt: {prompt}")

    # --- Set Image Quality based on FAST_MODE ---
    if settings.FAST_MODE:
        steps = 10
        sampler_name = "Euler"
        width = 512
        height = 512
    else:
        steps = 25
        sampler_name = "DPM++ 2M Karras"
        width = 1024
        height = 1024

    # --- API Payload ---
    payload = {
        "prompt": prompt,
        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face",
        "steps": steps,
        "cfg_scale": 7,
        "width": width,
        "height": height,
        "sampler_name": sampler_name,
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
        # We now return the definitive JSON string that our API route expects.
        result = {
            "image_base64": image_data,
            "final_prompt": prompt,
            "saved_path": str(file_path),
        }
        return json.dumps(result)
    else:
        print("API response did not contain image data.")
        error_result = {"error": "The image generation server did not return an image."}
        return json.dumps(error_result)
