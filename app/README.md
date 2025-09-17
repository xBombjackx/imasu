# Lovart AI - FastAPI Backend

This directory contains the core backend logic for the Lovart AI agentic image generation system. It's a FastAPI application responsible for orchestrating the AI workflow, from receiving user requests to coordinating with the LLM and image generation tools.

## Key Components

-   **`main.py`**: The main entry point for the FastAPI application. It initializes the app, sets up logging and middleware, and includes the API routers.

-   **`api/`**: This module contains the API endpoints.
    -   **`routes.py`**: Defines all the HTTP routes, such as `/agent/generate` and `/agent/variations`. It handles request validation (using Pydantic models), calls the appropriate agent or chain, and structures the final JSON response.

-   **`agent/`**: This module holds the core agentic logic built with LangChain.
    -   **`agent.py`**: Defines the main ReAct agent (`agent_executor`) that can reason and use tools.
    -   **`ideation.py`**: Defines the `ideation_chain`, a simpler chain used for brainstorming creative prompt variations.
    -   **`tools.py`**: Defines the custom tools available to the agent, such as the `generate_image` tool that communicates with the AUTOMATIC1111 API.

-   **`core/`**: This module is for application-wide settings and configuration.
    -   **`settings.py`**: Manages environment variables and application settings using Pydantic's `BaseSettings`. This is where API keys and external service URLs are configured.

## How It Works

1.  The Streamlit UI sends a request to an endpoint defined in `api/routes.py`.
2.  The endpoint function invokes either the `agent_executor` or the `ideation_chain` from the `agent/` module.
3.  The LangChain agent/chain communicates with the Ollama LLM to decide on a course of action.
4.  If the `generate_image` tool is chosen, the function in `agent/tools.py` is executed.
5.  This tool makes a REST API call to the AUTOMATIC1111 service.
6.  The final result (image and prompt) is passed back up the chain and returned by the FastAPI endpoint as a JSON response to the UI.
