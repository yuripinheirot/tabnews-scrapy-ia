import logging
from fastapi import FastAPI
from pydantic import BaseModel
from src.app_runner import AppRunner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()


class Url(BaseModel):
    urls: list[str]


class Text(BaseModel):
    text: str


@app.post("/get-by-urls")
async def read_root(payload: Url):
    try:
        logger.info(f"Received request to crawl. URLs received: {payload.urls}")
        app_runner = AppRunner(payload.urls)
        results = app_runner.run(payload.urls)

        return results
    except Exception as e:
        logger.error(f"An error occurred while enqueuing the spider. Error: {e}")
        return {"error": f"Failed to start spider: {str(e)}"}
