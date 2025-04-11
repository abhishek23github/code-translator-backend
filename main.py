from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    source_lang: str
    target_lang: str
    mode: str = "convert"  # convert | explain | fix
    verbose: bool = False

@app.post("/convert")
async def convert_code(req: CodeRequest):
    # 🔧 NEW: Prompt logic for "fix" mode
    if req.mode == "convert":
        prompt = (
            f"Convert the following code from {req.source_lang} to {req.target_lang}:\n\n{req.code}"
        )
    elif req.mode == "explain":
        prompt = (
            f"Explain what this {req.source_lang} code does step-by-step in simple terms:\n\n{req.code}"
        )
    elif req.mode == "fix":
        prompt = (
         f"Do not translate or convert the programming language.\n"
        f"The code below is written in {req.source_lang}. Your task is to:\n"
        f"- Fix any syntax or logical errors in the code\n"
        f"- Keep the language as strictly {req.source_lang}\n"
        f"- Use proper inline comments only where fixes were made (using {req.source_lang}'s comment syntax)\n"
        f"- Return only the corrected code\n"
        f"- Do not add explanations or rewrite in another language\n\n"
        f"---\n{req.code}\n---"
    )
    else:
        prompt = (
            f"Do not translate or convert the programming language.\n"
            f"The code below is written in {req.source_lang}. Your task is to:\n"
            f"- Fix any syntax or logical errors\n"
            f"- Keep the language as strictly {req.source_lang}\n"
            f"- Use proper inline comments only where fixes were made\n"
            f"- Return only the corrected code\n"
            f"- Do not add explanations or rewrite in another language\n\n"
            f"---\n{req.code}\n---"
        )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    converted_code = response.choices[0].message.content.strip()
    return {"converted_code": converted_code}
