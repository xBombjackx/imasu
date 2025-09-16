import requests
import base64
import os
import json
from langchain.tools import tool
from pydantic import BaseModel, Field


# --- TOOL INPUT SCHEMA ---
class ImageGenerationInput(BaseModel):
    """Input model for the generate_image tool."""

    prompt: str = Field(description="A detailed, professional prompt for the image.")
    negative_prompt: str = Field(description="A list of things to avoid in the image.")


# --- TOOL IMPLEMENTATION ---
@tool(args_schema=ImageGenerationInput)
def generate_image(prompt: str, negative_prompt: str) -> str:
    """
    Generates a high-quality image using a local AUTOMATIC1111 Stable Diffusion
    instance with professional settings and returns a confirmation message.
    """
    api_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # 💡 CHANGE: Incorporating advanced settings for higher quality output.
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": 30,
        "cfg_scale": 6,
        "width": 896,  # Using a professional portrait aspect ratio
        "height": 1152,
        "sampler_name": "DPM++ 2M SDE Karras",  # Using a different high-quality sampler
        "enable_hr": True,
        "hr_scale": 1.5,
        "hr_upscaler": "4xUltrasharp_4xUltrasharpV10",  # Make sure this upscaler is installed
        "hr_second_pass_steps": 15,  # Specific steps for the hires pass
        "denoising_strength": 0.33,  # Lower denoising for detail preservation
        "override_settings": {
            "sd_model_checkpoint": "juggernautXL_ragnarokBy.safetensors"
        },
    }

    print(f"--- Calling Image Generation Tool with payload: ---")
    print(json.dumps(payload, indent=2))

    try:
        # Increased timeout to 10 minutes (600 seconds) to handle slower generation
        response = requests.post(url=api_url, json=payload, timeout=600)

        if response.status_code == 500:
            error_details = response.text
            print(f"--- A1111 SERVER ERROR ---")
            print(error_details)
            return f"A1111 server returned a 500 error. Check the A1111 console for details. Response: {error_details}"

        response.raise_for_status()
        r = response.json()

        if "images" in r and r["images"]:
            image_data = r["images"][0]
            image_filename = f"img_{hash(image_data)}.png"
            output_path = os.path.join(output_dir, image_filename)

            with open(output_path, "wb") as f:
                f.write(base64.b64decode(image_data))

            final_output = f"Image successfully generated and saved to {output_path}"
            print(final_output)
            return final_output
        else:
            return "A1111 API call succeeded but returned no image data."

    except requests.exceptions.RequestException as e:
        error_message = f"Failed to connect to A1111 API: {e}"
        print(error_message)
        return error_message
