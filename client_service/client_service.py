from fastapi import FastAPI, Request, Header, HTTPException
import httpx
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

SUMMARY_SERVICE_URL = "http://localhost:8001/process"
DB_SAVE_URL = "http://localhost:8002/save"
DB_GET_URL = "http://localhost:8002/get"

@app.get("/")
def root():
    return {"message": "This is the Client Service for text summarization."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/submit")
async def submit_task(request: Request, authorization: str = Header(None)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    data = await request.json()
    text = data.get("text")

    if not text:
        raise HTTPException(status_code=400, detail="Text field is required")  

    async with httpx.AsyncClient() as client:
        try:
            summary_response = await client.post(SUMMARY_SERVICE_URL, json={"text": text})
            summary_response.raise_for_status()
            summary_data = summary_response.json()
            summary = summary_data.get("summary")

            save_response = await client.post(DB_SAVE_URL, json={"raw": text, "summary": summary})
            save_response.raise_for_status()
            save_data = save_response.json()
            saved_id = save_data.get("id")

            return {
                "status": "success",
                "summary": summary,
                "id": saved_id
            }

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Upstream service error: {e.response.text}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )

@app.get("/tasks")
async def get_tasks(authorization: str = Header(None)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    async with httpx.AsyncClient() as client:
        response = await client.get(DB_GET_URL)
        response.raise_for_status()
        return response.json()
