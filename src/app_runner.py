import crochet
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import logging
import time
import os
import json
from src.tabnews_spider import TabNewsSpider
from src.summarization_ai import summarization_ai

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
                        f"Timeout while waiting for the export file for the URL: {url}"
                    )
                    return {
                        "error": f"Timeout while waiting for the export file for the URL: {url}"
                    }
                logger.info(f"Waiting for the export file for the URL: {url}")
                time.sleep(0.5)

            with open(export_file, "r") as file:
                results.append(json.load(file))

        return results

    def summarize_results(self, results):
        summarized_results = []
        for result in results:
            summarized_result = {
                "url": result["url"],
                "title": result["title"],
                "content": result["content"],
                "resume_summarized": "",
            }

            if not result["content"].strip():
                summary = ""
            else:
                summary = summarization_ai(result["content"])

            summarized_result["resume_summarized"] = summary
            summarized_results.append(summarized_result)

        return summarized_results

    def run(self, urls):
        self.run_spider(urls)

        results = self.check_results()
        results_summarized = self.summarize_results(results)

        return {
            "message": "All urls were processed successfully.",
            "results": results_summarized,
        }
