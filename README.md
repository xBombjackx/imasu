# Lovart.ai - A Local Agentic AI Image Generation System

This project is a self-hosted, agentic system for AI image generation. It uses a robust, containerized architecture to separate reasoning, orchestration, and user interface components, allowing you to run a powerful AI art studio on your own machine.

## 🏛️ Core Architecture

The system is composed of three main services that communicate with each other:

1.  **`api` (Docker Service)**: The backend orchestrator that hosts the LangChain agent, receives requests from the UI, and coordinates with other services.
2.  **`ui` (Docker Service)**: The interactive web user interface where you enter prompts and view generated images.
3.  **`ollama` (Docker Service)**: The reasoning engine. This service runs a local Large Language Model (LLM) like Llama 3.1, which understands user intent, brainstorms ideas, and plans the steps for image generation.
4.  **AUTOMATIC1111 (Host Service)**: The specialist tool for image generation. It runs directly on your host machine to leverage GPU acceleration and exposes a REST API that the FastAPI backend calls.

```
┌───────────────────────────┐      ┌───────────────────────────┐
│      Your Computer        │      │      Docker Network       │
│  (Host Machine with GPU)  │      │                           │
│                           │      │   ┌───────────────────┐   │
│ ┌───────────────────────┐ │      │   │        api        │   │
│ │     AUTOMATIC1111     │ │      │   │-------------------│   │
│ │ (Image Gen Service)   │ │◄─────┼───│  FastAPI Backend  │   │
│ │    (localhost:7860)   │ │      │   │(Orchestrator)     │   │
│ └───────────────────────┘ │      │   └───────────────────┘   │
│                           │      │             ▲             │
└───────────────────────────┘      │             │             │
       ▲                         │             ▼             │
       │                         │   ┌───────────────────┐   │
       │                         │   │         ui        │   │
       │                         │   │      (UI)         │   │
       │                         │   └───────────────────┘   │
       │                         │             ▲             │
       │                         └─────────────┼─────────────┘
       │                                       │
┌───────────────────┐                          │
│      User       │                          │
│ (Web Browser)   ├──────────────────────────┘
│(localhost:8501) │
└───────────────────┘
```

## 📋 Prerequisites

-   **Docker & Docker Compose**: For running the containerized services.
-   **Git**: For cloning the repository.
-   **NVIDIA GPU**: Strongly recommended for running the AUTOMATIC1111 service with acceptable performance.

## 🚀 Getting Started

### Step 1: Set Up the Image Generation Service (AUTOMATIC1111)

The A1111 Web UI must run directly on your host machine to ensure it has full access to the GPU.

1.  **Install AUTOMATIC1111**: Follow the [official installation guide](https://github.com/AUTOMATIC1111/stable-diffusion-webui#installation-and-running).
2.  **Download a Model**: Download a Stable Diffusion model checkpoint (e.g., `v1-5-pruned-emaonly.safetensors`) and place it in the `stable-diffusion-webui/models/Stable-diffusion` directory.
3.  **Enable the API**: You **must** enable the REST API.
    -   **Windows**: Edit `webui-user.bat` and set `set COMMANDLINE_ARGS=--api`.
    -   **Linux/macOS**: Edit `webui-user.sh` and set `export COMMANDLINE_ARGS="--api"`.
4.  **Launch the Service**: Run the webui script. The server will be available at `http://127.0.0.1:7860`.

### Step 2: Configure Environment Variables

1.  **Create `.env` file**: In the project root, create a file named `.env`.
2.  **Add Configuration**: Add the following line to the `.env` file. You must replace `192.168.1.123` with your host machine's **local network IP address**.

    ```
    # .env
    A1111_URL="http://192.168.1.123:7860"
    ```

    > **Important**: Do not use `localhost` or `127.0.0.1`, as this address will not be accessible from within the Docker container.

### Step 3: Launch the Application with Docker Compose

With A1111 running and the `.env` file configured, launch the application stack:

```bash
docker compose up --build
```

This command will:

-   Build the `api` and `ui` Docker images using the `Dockerfile` and `Dockerfile.ui` respectively.
-   Pull the official `ollama/ollama` image.
-   Start the containers in the correct order.
-   The first time you run this, Ollama will download the default LLM model (`llama3.1:8b`), which may take a few minutes.

The application is now running!

## 💻 Usage

-   **Streamlit Web UI**: Open your browser and navigate to **http://localhost:8501**. This is the main interface for generating images.
-   **FastAPI Documentation**: To see the API documentation, navigate to **http://localhost:8000/docs**.
-   **Application Logs**: View the logs for the API and UI services by running `docker compose logs -f api` and `docker compose logs -f ui`.

## Project Structure

-   `app/`: Contains the FastAPI backend, including the LangChain agent, tools, and API routes.
-   `ui/`: Contains the Streamlit frontend application.
-   `tests/`: Contains the tests for the API and tools.
-   `output/`: The default directory where generated images are saved.
-   `CODE_REVIEW.md`: A detailed code review of the project.
-   `Dockerfile` & `Dockerfile.ui`: Define the Docker images for the backend and frontend.
-   `docker-compose.yml`: Orchestrates the deployment of all the services.
-   `requirements-api.txt` & `requirements-ui.txt`: The Python dependencies for the backend and frontend.

## 🛑 Stopping the Application

-   To stop all running services, press `Ctrl + C` in the terminal where `docker compose` is running.
-   To remove the containers and network, run: `docker compose down`.
-   Remember to also shut down the AUTOMATIC1111 service running on your host.