import logging
from fastapi import FastAPI, Response
from pydantic import BaseModel
from src.app_runner import AppRunner
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


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
