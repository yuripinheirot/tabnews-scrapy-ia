import logging  # Importa a biblioteca padrão para logging em Python
from fastapi import FastAPI  # Importa o FastAPI para criar a API
from pydantic import BaseModel  # Usado para validar o payload recebido (urls)
from scrapy.crawler import (
    CrawlerRunner,
)  # CrawlerRunner é usado para gerenciar os spiders sem bloquear a thread
from scrapy.utils.project import (
    get_project_settings,
)  # Pega as configurações do projeto Scrapy
from src.spiders.tabnews_spider import TabNewsSpider  # Importa seu spider específico
import crochet  # Biblioteca que integra o reactor do Scrapy com FastAPI (ou outros frameworks async)

# Inicializa o Crochet para garantir que o Twisted reactor esteja pronto para aceitar tarefas
crochet.setup()
logging.info("Crochet inicializado e reactor pronto para aceitar spiders.")

# Configura o nível de logging para INFO (vai mostrar logs gerais, avisos e erros)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Logging configurado e logger principal criado.")

# Cria a instância da aplicação FastAPI
app = FastAPI()
logger.info("FastAPI inicializada.")

# Cria uma instância global do CrawlerRunner com as configurações do projeto Scrapy
runner = CrawlerRunner(get_project_settings())
logger.info("CrawlerRunner criado com as configurações do projeto Scrapy.")


# Define o modelo de dados esperado no POST: uma lista de URLs
class Url(BaseModel):
    urls: list[str]


logger.info(
    "Modelo de payload 'Url' definido. Espera-se uma lista de URLs no campo 'urls'."
)


@app.post("/get-by-urls")
async def read_root(payload: Url):
    logger.info(f"Recebido pedido para crawlear. URLs recebidas: {payload.urls}")

    # Define uma função que será executada dentro do reactor (thread segura)
    @crochet.run_in_reactor
    def run_spider(urls):
        logger.info(f"Iniciando o spider TabNewsSpider com as URLs: {urls}")
        # Executa o spider passando as URLs recebidas
        return runner.crawl(TabNewsSpider, urls=urls)

    try:
        # Chama a função que enfileira o spider para execução no reactor
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
