from pathlib import Path
import json
import scrapy
from src.export_json import export_json


class TabNewsSpider(scrapy.Spider):
    name = "tabnews"

    def __init__(self, urls=None, *args, **kwargs):
        super(TabNewsSpider, self).__init__(*args, **kwargs)
        self.urls = urls or []

    def parse_title(self, response):
        title = response.css("h1::text").get()
        return title

    def parse_content(self, response):
        content = ""

        body = response.css(".markdown-body").get()
        bodyParsed = scrapy.Selector(text=body, type="html")

        for element in bodyParsed.css("p"):
            text = element.css("::text").get()
            if text:
                content += text + " "

        return content

    # Scrapy
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = {
            "content": "",
            "title": "",
            "url": response.url,
        }

        content["title"] = self.parse_title(response)
        content["content"] = self.parse_content(response)

        export_json(response.url, content)
