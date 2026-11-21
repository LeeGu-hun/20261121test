# ChatGPT를 활용한 챗봇 start
# from pathlib import Path
#
# from fastapi import FastAPI, HTTPException
# from fastapi.responses import HTMLResponse
# from pydantic import BaseModel, Field
# from openai import AsyncOpenAI
#
# app = FastAPI()
# client = AsyncOpenAI()
#
# BASE_DIR = Path(__file__).resolve().parent
#
#
# class ChatRequest(BaseModel):
#     message: str = Field(min_length=1, max_length=2000)
#     web_search: bool = False
#
#
# @app.get("/", response_class=HTMLResponse)
# def home():
#     return (BASE_DIR / "index.html").read_text(
#         encoding="utf-8"
#     )
#
#
# @app.post("/chat")
# async def chat(data: ChatRequest):
#     try:
#         params = {
#             "model": "gpt-4.1-mini",
#             "instructions": (
#                 "당신은 회사의 친절한 AI 업무 비서입니다. "
#                 "한국어로 정확하고 쉽게 답변하세요."
#             ),
#             "input": data.message,
#             "store": False
#         }
#
#         if data.web_search:
#             params["tools"] = [
#                 {"type": "web_search"}
#             ]
#
#         response = await client.responses.create(
#             **params
#         )
#
#         return {
#             "answer": response.output_text
#         }
#
#     except Exception as e:
#         print("API 오류:", repr(e))
#         raise HTTPException(
#             status_code=502,
#             detail="AI 응답에 실패했습니다. API 잔액과 서버 로그를 확인하세요."
#         )
# ChatGPT를 활용한 챗봇 end


import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

app = FastAPI(title="Gemini AI Chatbot")

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

BASE_DIR = Path(__file__).resolve().parent
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE_DIR / "index.html").read_text(
        encoding="utf-8"
    )


@app.post("/chat")
async def chat(data: ChatRequest):
    try:
        response = await client.aio.models.generate_content(
            model=MODEL,
            contents=data.message,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "당신은 회사의 AI 업무 비서입니다. "
                    "한국어로 쉽고 정확하게 답변하세요."
                )
            )
        )

        return {
            "answer": response.text or "답변을 생성하지 못했습니다."
        }

    except Exception as e:
        print("Gemini API 오류:", repr(e))
        raise HTTPException(
            status_code=502,
            detail="Gemini API 호출에 실패했습니다."
        )
