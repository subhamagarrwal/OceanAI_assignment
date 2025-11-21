# Autonomous QA Agent

## 🐳 Run with Docker (Recommended)

1. **Prerequisites:** Ensure Docker and Docker Compose are installed and **Docker Desktop is running**.

2. **Environment Setup:**
   The project requires API keys and Database credentials. I have provided a `.env.example` file with the necessary credentials for this assignment.
   
   ```bash
   # Rename the example file to .env
   cp .env.example .env
   ```

3. **Build and Run:**
   ```bash
   docker-compose up --build
   ```

4. **Access the App:**
   - **Frontend:** [http://localhost:8501](http://localhost:8501)
   - **Backend API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💻 Run Locally (Manual Setup)

### Backend
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   # Note: The entry point is api.py
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload
   ```
4. Access at `http://localhost:8000/docs`.

### Frontend 
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
- **`components/`**: Reusable UI components like the sidebar.
- **`utils/`**: Helper functions and the API client for communicating with the backend.

### Root Files
- **`docker-compose.yml`**: Orchestrates the multi-container Docker application.
- **`.env.example`**: Template for environment variables (API keys, DB credentials).
