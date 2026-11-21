from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from openai import AsyncOpenAI

app = FastAPI()
client = AsyncOpenAI()

BASE_DIR = Path(__file__).resolve().parent


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    web_search: bool = False


@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE_DIR / "index.html").read_text(
        encoding="utf-8"
    )


@app.post("/chat")
async def chat(data: ChatRequest):
    try:
        params = {
            "model": "gpt-4.1-mini",
            "instructions": (
                "당신은 회사의 친절한 AI 업무 비서입니다. "
                "한국어로 정확하고 쉽게 답변하세요."
            ),
            "input": data.message,
            "store": False
        }

        if data.web_search:
            params["tools"] = [
                {"type": "web_search"}
            ]

        response = await client.responses.create(
            **params
        )

        return {
            "answer": response.output_text
        }

    except Exception as e:
        print("API 오류:", repr(e))
        raise HTTPException(
            status_code=502,
            detail="AI 응답에 실패했습니다. API 잔액과 서버 로그를 확인하세요."
        )
