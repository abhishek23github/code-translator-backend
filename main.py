from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai  # ✅ Make sure this is here BEFORE calling openai.api_key

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS setup for frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class CodeRequest(BaseModel):
    prompt: str
    language: str
    mode: str  # convert, fix, explain

# POST /convert endpoint
@app.post("/convert")
async def convert_code(request: CodeRequest):
    if request.mode == "convert":
        prompt = f"Convert the following code to {request.language}:\n\n{request.prompt}"
    elif request.mode == "fix":
        prompt = f"Fix the following code. Respond only with corrected code and comment the fixes made:\n\n{request.prompt}"
    elif request.mode == "explain":
        prompt = f"Explain this code line by line:\n\n{request.prompt}"
    else:
        return {"error": "Invalid mode"}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful code assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return {"output": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": str(e)}
