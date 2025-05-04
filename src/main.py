from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from src.spiders.tabnews_spider import TabNewsSpider
from scrapy.crawler import CrawlerProcess

app = FastAPI()


class Url(BaseModel):
    urls: list[str]


@app.post("/")
def read_root(payload: Url):
    process = CrawlerProcess()
    process.crawl(TabNewsSpider, urls=payload.urls)
    process.start()

    return {
        "message": "Foram executados os spiders nas urls: " + ", ".join(payload.urls)
    }
