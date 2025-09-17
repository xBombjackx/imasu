# Lovart AI - Streamlit UI

This directory contains the user interface for the Lovart AI application, built using the Streamlit framework. The UI provides an interactive, web-based experience for users to generate AI images.

## Key Components

-   **`app.py`**: This is the main and only file for the Streamlit application. It is responsible for:
    -   **Rendering the UI**: Laying out the page title, input forms, buttons, and spinners using Streamlit components.
    -   **State Management**: Using `st.session_state` to hold the results of the image generation process, allowing the gallery to persist across interactions.
    -   **API Communication**: Defining functions (`get_prompt_variations`, `generate_image`) that send HTTP requests to the FastAPI backend.
    -   **Displaying Results**: Rendering the generated images and their final prompts in a clean, multi-column gallery format.

## How It Works

1.  The user enters a simple idea into the text input field and clicks the "Generate Concepts" button.
2.  The `get_prompt_variations` function is called, which sends a POST request to the `/agent/variations` endpoint of the FastAPI backend.
3.  Once the creative variations are received, the UI displays a status update.
4.  The application then iterates through each variation, calling the `generate_image` function for each one. This function sends a POST request to the `/agent/generate` endpoint.
5.  As each image is generated, the base64-encoded image data and the final prompt are received from the API.
6.  The image is decoded and displayed in the UI, and the result is stored in `st.session_state.results`.
7.  The final gallery is displayed at the bottom of the page.

## Configuration

The UI determines the backend API's location via the `API_BASE_URL` environment variable.

-   **When running with Docker Compose**: This is set automatically to `http://lovart_app:8000` to enable communication between the UI and backend containers.
-   **When running locally for development**: If the environment variable is not set, it defaults to `http://localhost:8000`.
