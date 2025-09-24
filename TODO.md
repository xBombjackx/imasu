# TODO

This file outlines areas of improvement and potential issues found in the codebase.

## General Recommendations

*   **Configuration Management**: The use of `os.getenv` is spread across multiple files. Centralizing configuration in `app/core/settings.py` would be beneficial. This could be achieved by creating a `Settings` class that loads all environment variables and is then used throughout the application.
*   **Error Handling**: The error handling in the API and agent is minimal. Implementing more robust error handling would improve the application's stability. For example, adding `try-except` blocks around API calls and other potentially failing operations.
*   **Logging**: There is no logging implemented. Adding a structured logging solution (e.g., using Python's `logging` module) would make debugging and monitoring the application easier.
*   **Code Duplication**: There is some code duplication that could be refactored. For example, the image generation logic in `app/agent/tools.py` and `scripts/test_a1111.py`.
*   **Testing**: The test coverage is low. Adding more unit and integration tests would improve the code quality and reduce the risk of regressions.

## File-specific Issues

### `app/main.py`

*   The `description` in the `FastAPI` app is a bit generic. It could be improved to be more descriptive of the API's purpose.

### `app/agent/agent.py`

*   The `Agent` class has a hardcoded `model` ("mistral"). This should be configurable.
*   The `ideation_agent` and `image_agent` are created in the `__main__` block. This makes the file difficult to import and reuse. The agent creation should be moved to a function.

### `app/agent/ideation.py`

*   The `IdeationAgent` class has a hardcoded `model`. This should be configurable.
*   The `prompt` is a bit long and could be broken down into smaller, more manageable parts.

### `app/agent/tools.py`

*   The `generate_image` function has a hardcoded `api_url`. This should be configurable.
*   The function uses `requests.post` without any error handling. This could lead to unhandled exceptions if the API call fails.
*   The function writes the image to a hardcoded path (`output/`). This should be configurable.

### `app/api/routes.py`

*   The `/generate` endpoint does not have any input validation. It should validate the `prompt` to ensure it's not empty.
*   The endpoint returns a plain text response. It would be better to return a JSON response with the image URL or the image itself (e.g., base64 encoded).

### `app/core/settings.py`

*   This file is empty. It should be used to manage the application's settings.

### `scripts/test_a1111.py`

*   This script seems to be for testing the Automatic1111 API. It has hardcoded values for `prompt`, `negative_prompt`, and `seed`. These should be configurable, for example, by using command-line arguments.
*   The script writes the output to a hardcoded path (`c:/Users/toast/repos/imasu/output/`). This should be configurable.

### `scripts/test_ollama.py`

*   This script is for testing the Ollama API. It has a hardcoded `model` ("mistral"). This should be configurable.

### `tests/test_api.py`

*   The tests are minimal and only check if the endpoints return a 200 status code. They should be expanded to check the response content.

### `tests/test_tools.py`

*   The tests are minimal and only check if the `generate_image` function returns a non-empty response. They should be expanded to check the image content or at least the image format.

### `ui/app.py`

*   The Streamlit app has a hardcoded API URL (`http://localhost:8000/generate`). This should be configurable.
*   The app displays the generated image but doesn't provide any way to save or download it.

### `Dockerfile`

*   The Dockerfile is quite complex and could be simplified. For example, it could use a multi-stage build to reduce the final image size.
*   It exposes port 8000, but the `CMD` runs `uvicorn` on port 80. This is inconsistent.

### `Dockerfile.ollama`

*   This Dockerfile is for the Ollama service. It seems to be a standard Ollama Dockerfile. No major issues found.

### `Dockerfile.ui`

*   This Dockerfile is for the Streamlit UI. It exposes port 8501, which is the standard Streamlit port. No major issues found.

### `docker-compose.yml`

*   The `docker-compose.yml` file is well-structured.
*   The `api` service depends on `ollama`, which is good.
*   The `ui` service depends on `api`, which is also good.
*   The volumes are correctly configured to mount the local code into the containers.
