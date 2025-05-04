from pathlib import Path
import json
import scrapy


class TabNewsSpider(scrapy.Spider):
    name = "tabnews"

    def __init__(self, urls=None, *args, **kwargs):
        super(TabNewsSpider, self).__init__(*args, **kwargs)
        self.urls = urls or []

    # Utils

    def export_json(self, items, filename):
        with open(filename, "w") as f:
            json.dump(items, f, ensure_ascii=False)

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
                content += " " + text

        return content

    def create_file_name(self, url):
        return f"output/{url.split('/')[-1]}.json"

    def export_content(self, content, filename):
        output_dir = Path("output")
        if not output_dir.exists():
            output_dir.mkdir(parents=True)

        self.export_json(content, filename)

    # Scrapy

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = {
            "title": "",
            "content": "",
        }

        content["title"] = self.parse_title(response)
        content["content"] = self.parse_content(response)

        filename = self.create_file_name(response.url)
        self.export_content(content, filename)
