import scrapy
import requests
from scrapy.utils.sitemap import Sitemap


class RecipeSpider(scrapy.Spider):
    name = "recipe"
    sitemap_url = "https://www.rewe.de/sitemaps/sitemap-rezepte.xml"

    def read_sitemap_urls(self):
        response = requests.get(
            self.sitemap_url,
            headers={"Accept": "*/*", "User-Agent": "Scrapy"},
        )
        s = Sitemap(response.content)
        return list(map(lambda i: i["loc"], s))

    def read_sitemap_from_file(self):
        with open("sitemap-recipes.xml", "rb") as read_sitemap:
            s = Sitemap(read_sitemap.read())
            return list(map(lambda i: i["loc"], s))

    def start_requests(self):
        urls = self.read_sitemap_from_file()[9719:]
        for url in urls:
            yield scrapy.Request(url, self.parse, meta={"playwright": True})

    def parse(self, response):
        recipe_schema = response.xpath('//*[@id="recipe-schema"]/text()').get()
        recipe_html = response.xpath("/html/body/div[2]/div[1]").get()
        yield {
            "url": response.url,
            "recipe_schema": recipe_schema,
            "recipe_html": recipe_html,
        }
