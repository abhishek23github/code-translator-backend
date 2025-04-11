from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Set API key via environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

# Allow frontend to call this API (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body structure
class CodeRequest(BaseModel):
    prompt: str
    language: str
    mode: str  # convert, fix, explain

@app.post("/convert")
async def convert_code(request: CodeRequest):
    user_prompt = ""

    if request.mode == "convert":
        user_prompt = f"Convert this code to {request.language}:\n\n{request.prompt}"
    elif request.mode == "fix":
        user_prompt = f"Fix the following code:\n\n{request.prompt}\n\nReturn fixed code only with comments on the fixes made."
    elif request.mode == "explain":
        user_prompt = f"Explain the following code line by line:\n\n{request.prompt}"
    else:
        return {"error": "Invalid mode"}

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
        )

        return {"output": response.choices[0].message.content.strip()}

    except Exception as e:
        return {"error": str(e)}
