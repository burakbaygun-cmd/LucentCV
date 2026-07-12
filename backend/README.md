# LucentCV 2.0 Backend

This is the FastAPI backend for LucentCV, implementing Clean Architecture and relying on Supabase for data persistence and Google Gemini for AI functionalities.

## Requirements
- Python 3.12+
- Supabase Project

## Local Setup
1. Create a `.env` file based on `.env.example`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints
View the full Swagger documentation at `http://localhost:8000/docs` after starting the server.

## Docker Setup
Alternatively, use `docker-compose up -d` from the root directory to spin up the entire application stack.
