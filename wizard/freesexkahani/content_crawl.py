from odoo import models, fields, api
from bs4 import BeautifulSoup
import requests


class FreeSexKahaniContentCrawl(models.TransientModel):
    _name = "free.sex.kahani.content.crawl"
    _description = "Free Sex Kahani Content Crawl"

    url = fields.Text(string="URL")

    def trigger_crawl(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')

        content = soup.find("div", class_="entry-content")
        recs = content.find_all("p")

        for rec in recs:
            print(rec)




