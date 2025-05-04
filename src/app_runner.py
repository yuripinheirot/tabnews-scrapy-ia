import crochet
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import logging
import time
import os
import json
from src.spiders.tabnews_spider import TabNewsSpider

logger = logging.getLogger(__name__)
crochet.setup()
runner = CrawlerRunner(get_project_settings())


class AppRunner:
    def __init__(self, urls):
        self.runner = runner
        self.urls = urls

    @crochet.run_in_reactor
    def run_spider(self, urls):
        return self.runner.crawl(TabNewsSpider, urls=urls)

    def check_results(self):
        results = []

        for url in self.urls:
            export_file = f"output/{url.split('/')[-1]}.json"
            start_time = time.time()
            while not os.path.exists(export_file):
                if time.time() - start_time > 15:
                    logger.error(
                        f"Timeout ao esperar pelo arquivo de exportação para a URL: {url}"
                    )
                    return {
                        "error": f"Timeout ao esperar pelo arquivo de exportação para a URL: {url}"
                    }
                logger.info(f"Aguardando exportação do arquivo para a URL: {url}")
                time.sleep(0.5)

            with open(export_file, "r") as file:
                results.append(json.load(file))

        return results

    def run(self, urls):
        self.run_spider(urls)

        results = self.check_results()

        return {
            "message": "Todos os spiders foram processados com sucesso.",
            "results": results,
        }
