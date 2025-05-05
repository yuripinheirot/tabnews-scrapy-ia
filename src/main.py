import logging
import os
from fastapi import FastAPI, Response, Request, Depends, HTTPException
from pydantic import BaseModel
from src.app_runner import AppRunner
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("X-API-Key")
    expected_api_key = os.getenv("API_KEY")

    if api_key != expected_api_key:
        logger.warning("Invalid or missing API key")
        return Response(
            content='{"detail": "Invalid or missing API key"}',
            status_code=401,
            media_type="application/json",
        )

    return await call_next(request)


app.middleware("http")(api_key_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Url(BaseModel):
    urls: list[str]


class Text(BaseModel):
    text: str


@app.post("/get-by-urls")
async def read_root(response: Response, payload: Url):
    try:
        logger.info(f"Received request to crawl. URLs received: {payload.urls}")
        app_runner = AppRunner(payload.urls)
        results = app_runner.run(payload.urls)

        return results
    except Exception as e:
        logger.error(e)
        response.status_code = 500
        return {"error": f"Failed to start spider: {str(e)}"}
