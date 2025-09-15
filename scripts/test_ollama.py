import json
import ollama


try:
    response = ollama.chat(
        model="mistral:7b", messages=[{"role": "user", "content": "hi"}]
    )

    print("API Connection Successful!")
    print("---")
    # Pretty-print the JSON response content
    print(json.dumps(response.model_dump(), indent=2))
    print("--- Message Content ---")
    print(response["message"]["content"])

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure the Ollama application or server is running.")
