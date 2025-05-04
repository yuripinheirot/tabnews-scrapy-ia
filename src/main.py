import logging
from fastapi import FastAPI
from pydantic import BaseModel
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from src.spiders.tabnews_spider import TabNewsSpider
import crochet
from src.ai.bart_large import bart_large
import os
import time
import json
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
        logger.info(f"Recebido pedido para crawlear. URLs recebidas: {payload.urls}")
        app_runner = AppRunner(payload.urls)
        results = app_runner.run(payload.urls)

        return results
    except Exception as e:
        logger.error(f"Ocorreu um erro ao tentar enfileirar o spider. Erro: {e}")
        return {"error": f"Falha ao iniciar spider: {str(e)}"}


@app.post("/process-text")
async def process_text(payload: Text):
    logger.info(f"Recebido pedido para processar texto...")

    resume = bart_large(payload.text)

    return {"message": "Texto processado com sucesso.", "resume": resume}
