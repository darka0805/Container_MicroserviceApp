# Text summarization Microservice_app 

1) This project is a set of FastAPI microservices that perform text summarization using Google Gemini API, store results, and expose an authenticated client endpoint.
2) Project structure


![image](https://github.com/user-attachments/assets/3983e011-02e9-496b-a3d2-ab65a140f14b)

Setup Instructions
1. Create accounts and set your keys
GEMINI_API_KEY=your_google_gemini_api_key
API_TOKEN=mysecrettoken
2. Install dependencies
!pip install fastapi uvicorn python-dotenv httpx google-generativeai

Token-Based Authentication
The /submit endpoint in client_service.py requires a token:
You must include an Authorization header:
"Authorization: Bearer secret_token"

Run Services Individually
- Business Service(uvicorn business_service:app --port 8001 --reload)
- DB Service(uvicorn db_service:app --port 8002 --reload)
- Client Service(uvicorn client_service:app --port 8000 --reload)
  Or you can run all at once 
python run_all.py

Request Flow
Client → (Client Service:8000) → [Business Service:8001] (summarize using Gemini API) → [Database Service:8002] (save summary) → [Client] (return summary + ID)
