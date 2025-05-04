import logging
from fastapi import FastAPI
from pydantic import BaseModel
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from src.spiders.tabnews_spider import TabNewsSpider
import crochet
from src.ai.bart_large import bart_large

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
        return {
            "message": "Spider enfileirado para as URLs: " + ", ".join(payload.urls)
        }
    except Exception as e:
        logger.error(f"Ocorreu um erro ao tentar enfileirar o spider. Erro: {e}")
        return {"error": f"Falha ao iniciar spider: {str(e)}"}


@app.post("/process-text")
async def process_text(payload: Text):
    logger.info(f"Recebido pedido para processar texto...")

    resume = bart_large(payload.text)

    return {"message": "Texto processado com sucesso.", "resume": resume}
