# OceanAI- Assignemnt 3-Autonomous QA Agent

## Run

### Prerequisites
The project requires API key for Groq. I have provided a `.env.example` file with the necessary credentials for this assignment.

```bash
# Rename the example file to .env in root 
cp .env.example .env
```

### Option 1: Docker (Recommended)
The easiest way to run the entire application stack (backend + frontend) is using Docker Compose:

1. Ensure Docker and Docker Compose are installed on your system.Open Docker on your system to ensure Docker Engine is running.
2. From the project root directory, run:
   ```bash
   docker-compose up --build
   ```
3. Access the application:
   - **Frontend (Streamlit)**: `http://localhost:8501`
   - **Backend (FastAPI)**: `http://localhost:8000`
   - **API Documentation**: `http://localhost:8000/docs`

4. To stop the services:
   ```bash
   docker-compose down
   ```

The backend Docker image has been optimized from 8.24GB to 971MB  by removing the redundant `sentence-transformers` dependency (because having that meant docker would also install heavier transitory dependencies) and using ChromaDB's built-in embeddings.

### Option 2: Manual Setup

#### Backend
1. Go to `backend` directory:
   ```bash
   cd backend
   ```
2. Install the dependencies defined in requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   # Note: The entry point is api.py
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload
   ```
4. Access at `http://localhost:8000/`.

#### Frontend 
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Access at `http://localhost:8501`.

##LLM used

We need LLM not only for the test cases but also for the code generation for any of the postive or negetive test cases. For this purpose, I used Llama 3.3-70b-versatile from Groq. I used Groq since it provides high speed inference using their hardware.I initialized my Groq client in the backend/llm/groq_client.py file.

## 📂 Project Structure

The project is organized into two main components:

### `backend/` (FastAPI)
Handles the core logic, RAG pipeline, and LLM interactions.
- **`api.py`**: The main entry point for the FastAPI server.
- **`core/`**: Contains the core agent logic (`agent.py`) and code generation modules (`code_gen.py`).
- **`rag/`**: Manages the Retrieval-Augmented Generation pipeline, including database connections (`database.py`), ingestion (`ingestion.py`), and retrieval (`retriever.py`).
- **`llm/`**: Contains the **Groq Client** (`groq_client.py`) which interfaces with the Groq API for high-speed inference using Llama 3 models.
- **`config/`**: Configuration settings and environment variable management.

### `frontend/` (Streamlit)
Provides the user interface for interacting with the agent.
- **`app.py`**: The main entry point for the Streamlit application.
- **`views/`**: Separate modules for different UI phases (Ingestion, Planning, Coding).
- **`components/`**: Reusable UI components like the sidebar in the Streamlit app.
- **`utils/`**: Helper functions and the API client for communicating with the backend.

### Root Files
- **`.env.example`**: Template for environment variables (API keys, DB credentials).

## Deployment 

### Local Development
Users can deploy the frontend and backend locally using either:
- **Docker Compose** (recommended): Run `docker-compose up --build` from the project root
- **Manual setup**: Follow the installation steps in the "Run" section above

### Production Deployment
Have deployed the frontend and the backend seperately for the sake of convenience, alongside using AWS Lambda function and Eventbridge scehduler to avoid the free tiered deployed Render web service from winding down(Render free tiered web service winds down after 15 minutes of activity.)
-**`Deployed frontend`**: https://oceanai-assignment-yrkg.onrender.com/
-**`Deployed backend`**:  https://oceanai-backend.onrender.com/  
