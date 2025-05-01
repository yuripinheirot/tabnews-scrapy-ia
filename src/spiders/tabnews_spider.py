from pathlib import Path
import json
import scrapy


class TabNewsSpider(scrapy.Spider):
    name = "tabnews"

    def start_requests(self):
        urls = [
            "https://www.tabnews.com.br/gabrieldsmiranda/tomei-bronca-por-fazer-monorepo",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def export_json(self, items, filename):
        with open(filename, "w") as f:
            json.dump(items, f, ensure_ascii=False)

    def parse_title(self, response):
        title = response.css("h1::text").get()
        return title

    def parse_content(self, response):
        content = []

        body = response.css(".markdown-body").get()
        bodyParsed = scrapy.Selector(text=body, type="html")

        for element in bodyParsed.css("p"):
            text = element.css("::text").get()
            if text:
                content.append(text)

        return content

    def create_file_name(self, title):
        return f"output/tabnews-{title.lower().replace(' ', '-')}.json"

    def export_content(self, content):
        output_dir = Path("output")
        if not output_dir.exists():
            output_dir.mkdir(parents=True)

        filename = self.create_file_name(content["title"])
        self.export_json(content, filename)

    def parse(self, response):
        content = {
            "title": "",
            "content": [],
        }

        content["title"] = self.parse_title(response)
        content["content"] = self.parse_content(response)

        self.export_content(content)
