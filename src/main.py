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

crochet.setup()
logging.info("Crochet inicializado e reactor pronto para aceitar spiders.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Logging configurado e logger principal criado.")

app = FastAPI()
logger.info("FastAPI inicializada.")

runner = CrawlerRunner(get_project_settings())
logger.info("CrawlerRunner criado com as configurações do projeto Scrapy.")


class Url(BaseModel):
    urls: list[str]


class Text(BaseModel):
    text: str


logger.info(
    "Modelo de payload 'Url' definido. Espera-se uma lista de URLs no campo 'urls'."
)


@app.post("/get-by-urls")
async def read_root(payload: Url):
    logger.info(f"Recebido pedido para crawlear. URLs recebidas: {payload.urls}")

    @crochet.run_in_reactor
    def run_spider(urls):
        logger.info(f"Iniciando o spider TabNewsSpider com as URLs: {urls}")
        return runner.crawl(TabNewsSpider, urls=urls)

    try:
        run_spider(payload.urls)
        logger.info(
            f"Spider foi enfileirado com sucesso para as URLs: {payload.urls}. O processamento acontecerá em background."
        )

        # Check for existing files and wait with timeout
        results = []
        for url in payload.urls:
            export_file = f"output/{url.split('/')[-1]}.json"
            start_time = time.time()
            while not os.path.exists(export_file):
                if time.time() - start_time > 60:
                    logger.error(
                        f"Timeout ao esperar pelo arquivo de exportação para a URL: {url}"
                    )
                    return {
                        "error": f"Timeout ao esperar pelo arquivo de exportação para a URL: {url}"
                    }
                logger.info(f"Aguardando exportação do arquivo para a URL: {url}")
                time.sleep(1)  # Wait for 1 second before checking again
            with open(export_file, "r") as file:
                results.append(json.load(file))

        return {
            "message": "Todos os spiders foram processados com sucesso.",
            "results": results,
        }

    except Exception as e:
        logger.error(f"Ocorreu um erro ao tentar enfileirar o spider. Erro: {e}")
        return {"error": f"Falha ao iniciar spider: {str(e)}"}


@app.post("/process-text")
async def process_text(payload: Text):
    logger.info(f"Recebido pedido para processar texto...")

    resume = bart_large(payload.text)

    return {"message": "Texto processado com sucesso.", "resume": resume}
