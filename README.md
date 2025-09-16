# **Lovart.ai PoC: A Local Agentic AI System**

This project is a proof-of-concept for a local, self-hosted agentic system for AI image generation. It uses a multi-component architecture that separates reasoning, orchestration, and specialized tools into distinct, communicating services.

## **🏛️ Core Architecture**

The system is built on three fundamental primitives, ensuring a clean separation of concerns:

1. **The Orchestrator (FastAPI)**: The central application server that receives user requests, hosts the LangChain agent, and coordinates the other components via API calls.  
2. **The Reasoning Engine (Ollama)**: A locally hosted Large Language Model (LLM), such as llama3.1:8b, that understands user intent, plans steps, and decides which tools to use.  
3. **The Specialist Tool (AUTOMATIC1111)**: A dedicated service for text-to-image generation that exposes a REST API for the Orchestrator to call.

This project uses **LangChain** as the "glue" to connect the Orchestrator to the Reasoning Engine and the Specialist Tools, enabling the agentic workflow.

## **📋 Prerequisites**

Before you begin, ensure you have the following installed on your system:

* **Docker & Docker Compose**: For running the containerized services.  
* **Git**: For cloning the repository.  
* **NVIDIA GPU**: Recommended for running the AUTOMATIC1111 image generation service with acceptable performance.

## **🚀 Getting Started**

Follow these steps to set up and run the entire application stack.

### **Step 1: Clone the Repository**

First, clone the project repository to your local machine:

git clone \<your-repository-url\>  
cd \<your-repository-name\>

### **Step 2: Set Up the Image Generation Service (AUTOMATIC1111)**

The AUTOMATIC1111 Web UI will run directly on your host machine to ensure it has full access to the GPU.

1. **Install AUTOMATIC1111**: Follow the official installation guide to set up the stable-diffusion-webui.  
2. **Download a Model**: Download a Stable Diffusion model checkpoint (e.g., v1-5-pruned-emaonly.safetensors) and place it in the stable-diffusion-webui/models/Stable-diffusion directory.  
3. **Enable the API**: You **must** enable the REST API for the Orchestrator to communicate with it.  
   * **On Windows**: Edit the webui-user.bat file and set the command-line arguments:  
     set COMMANDLINE\_ARGS=--api

   * **On Linux/macOS**: Edit the webui-user.sh file and set the command-line arguments:  
     export COMMANDLINE\_ARGS="--api"

4. **Launch the Service**: Run the webui-user.bat or webui-user.sh script. Wait for it to complete the setup and start the server, which will be available at http://127.0.0.1:7860.

### **Step 3: Configure Environment Variables**

The application uses a .env file to manage configuration.

1. **Create the File**: In the root of the project directory, create a new file named .env.  
2. **Add Configuration**: Add the following line to the .env file. If your AUTOMATIC1111 service is running on a different IP address (e.g., another machine on your network), update the URL accordingly.  
   \# .env  
   A1111\_URL="http://192.168.1.123:7860"

   ***Note***: *Replace* 192.168.1.123 with your host machine's actual local network *IP address. Do not use localhost or 127.0.0.1 as this will not be accessible from within the Docker container.*

### **Step 4: Launch the Application with Docker Compose**

With AUTOMATIC1111 running and the .env file configured, you can now launch the rest of the stack using Docker Compose.

Open your terminal in the project root and run:

docker-compose up \--build

This command will:

* Build the custom Docker image for the lovart\_app service using the Dockerfile.  
* Pull the official ollama/ollama image for the Reasoning Engine.  
* Create and start the containers for both the FastAPI/Streamlit application and the Ollama service.  
* The first time you run this, Ollama will download the llama3.1:8b model, which may take some time.

## **💻 Usage**

Once the containers are running, you can access the application:

* **Streamlit Web UI**: Open your web browser and navigate to **http://localhost:8501**. This is the main user interface for generating images.  
* **FastAPI Documentation**: To see the available API endpoints, navigate to **http://localhost:8000/docs**.

## **🛑 Stopping the Application**

To stop all the running services, press Ctrl \+ C in the terminal where docker-compose is running.

To remove the containers and the network, run:

docker-compose down

Remember to also shut down the AUTOMATIC1111 service running on your host machine.