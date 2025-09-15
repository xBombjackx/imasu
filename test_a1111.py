import requests
import base64
import os

# The URL for the AUTOMATIC1111 API
A1111_URL = "http://127.0.0.1:7860"
TXT2IMG_ENDPOINT = f"{A1111_URL}/sdapi/v1/txt2img"

# The output directory for generated images
OUTPUT_DIR = "generated_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# The payload defines the parameters for image generation
payload = {
    "prompt": "a photorealistic portrait of a majestic lion, cinematic lighting",
    "negative_prompt": "cartoon, drawing, sketch, blurry, ugly",
    "steps": 25,
    "width": 512,
    "height": 512,
    "cfg_scale": 7.5,
    "sampler_name": "Euler a",
}

print("Sending request to AUTOMATIC1111 API...")

try:
    # Send the POST request to the API
    response = requests.post(url=TXT2IMG_ENDPOINT, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    r = response.json()

    # The API returns images as a list of Base64-encoded strings
    if "images" in r and len(r["images"]) > 0:
        # Get the first image from the list
        image_data_base64 = r["images"][0]

        # Decode the Base64 string into bytes
        image_data = base64.b64decode(image_data_base64)

        # Define the output file path
        output_path = os.path.join(OUTPUT_DIR, "test_output.png")

        # Write the image bytes to a file
        with open(output_path, "wb") as f:
            f.write(image_data)

        print(f"Image successfully generated and saved to: {output_path}")
    else:
        print("API response did not contain any images.")
        print("Response JSON:", r)

except requests.exceptions.RequestException as e:
    print(f"An error occurred while calling the API: {e}")
    print("Please ensure the AUTOMATIC1111 Web UI is running with the --api flag.")
