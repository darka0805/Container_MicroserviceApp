from fastapi import FastAPI
import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
CLIENT_SERVICE_URL = os.getenv("CLIENT_SERVICE_URL", "http://client_service:8000")

@app.on_event("startup")
async def startup_event():
    async def periodic_call():
        while True:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{CLIENT_SERVICE_URL}/health")
                    print(f"Health check response: {response.json()}")
            except Exception as e:
                print(f"Error during health check: {e}")
            await asyncio.sleep(10)
    asyncio.create_task(periodic_call())

@app.get("/health")
def health():
    return {"status": "scheduler running"}
