from fastapi import FastAPI, Request
import os
import google.generativeai as genai
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@app.get("/")
def root():
    return {"message": "This is the Text Summarization Service using Gemini model."}

@app.get("/health")
def health():
    return {"status": "ok"}

def summarize_text(text: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please summarize the following text:\n\n{text}"])
        return response.text.strip()
    except Exception as e:
        return f"Error occurred during summarization: {str(e)}"

@app.post("/process")
async def process_task(request: Request):

    data = await request.json()
    text = data.get("text")  
    
    if not text:
        return {"error": "Text is required."}

    try:
        summary = summarize_text(text)
        if summary:
            return {"summary": summary}
        else:
            return {"error": "No valid summary returned from the Gemini model."}

    except Exception as e:
        return {"error": f"Failed to process task: {str(e)}"}
