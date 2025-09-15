import base64
import os
import requests
from langchain_core.tools import tool
from app.core.config import A1111_URL, OUTPUT_DIR


@tool
def generate_image(prompt: str) -> str:
    """
    Use this tool to generate an image based on a detailed textual description.
    This tool calls a local Stable Diffusion API to create the image.
    The input should be a rich, descriptive prompt suitable for an image generation model.
    """
    print(f"--- Calling Image Generation Tool with prompt: '{prompt}' ---")

    # Ensure the output directory exists
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

            # Use a hash of the prompt for a unique filename
            output_filename = f"img_{hash(prompt)}.png"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_path, "wb") as f:
                f.write(image_data)

            return f"Image successfully generated and saved to {output_path}"
        else:
            return "Error: API response did not contain an image."

    except Exception as e:
        print(f"Error calling AUTOMATIC1111 API: {e}")
        return f"Error: Failed to generate image. The service may be down. Details: {str(e)}"
