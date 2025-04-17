from fastapi import FastAPI, Request
import uuid

app = FastAPI()
db = {}

@app.get("/")
def root():
    return {"message": "This is the Database Service for storing tasks."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/save")
async def save_task(request: Request):
    data = await request.json()
    task_id = data.get("id") or str(uuid.uuid4())
    db[task_id] = {
        "raw": data.get("raw"),
        "summary": data.get("summary")
    }
    return {"status": "saved", "id": task_id}

@app.get("/get")
def get_all():
    return db
