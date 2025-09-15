import base64
import os
import requests
import json  # <-- Add this import
from langchain_core.tools import tool
from app.core.config import A1111_URL, OUTPUT_DIR


@tool
def generate_image(prompt: str) -> str:
    """
    Use this tool to generate an image based on a detailed textual description.
    This tool calls a local Stable Diffusion API to create the image.
    The input should be a rich, descriptive prompt suitable for an image generation model.
    Returns a JSON string containing the result message and the filename of the created image.
    """
    print(f"--- Calling Image Generation Tool with prompt: '{prompt}' ---")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, ugly, deformed, watermark, text",
        "steps": 28,
        "width": 512,
        "height": 512,
        "cfg_scale": 7.0,
        "sampler_name": "DPM++ 2M Karras",
    }

    try:
        response = requests.post(url=f"{A1111_URL}/sdapi/v1/txt2img", json=payload)
        response.raise_for_status()
        r = response.json()

        if "images" in r and len(r["images"]) > 0:
            image_data = base64.b64decode(r["images"][0])
            output_filename = f"img_{hash(prompt)}.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_path, "wb") as f:
                f.write(image_data)

            # --- MODIFICATION START ---
            # Return a JSON string with both a message and the filename
            result = {
                "message": f"Image successfully generated and saved to {output_path}",
                "image_filename": output_filename,
            }
            return json.dumps(result)
            # --- MODIFICATION END ---
        else:
            return json.dumps(
                {
                    "message": "Error: API response did not contain an image.",
                    "image_filename": None,
                }
            )

    except Exception as e:
        print(f"Error calling AUTOMATIC1111 API: {e}")
        return json.dumps(
            {
                "message": f"Error: Failed to generate image. Details: {str(e)}",
                "image_filename": None,
            }
        )
