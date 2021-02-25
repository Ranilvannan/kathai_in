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

        obj = self.env["kathai.in.story"].search([("url", "=", self.url)])

        content = []
        count = 1
        for rec in recs:
            content.append((0, 0, {"order_seq": count,
                                   "paragraph": rec.text}))
            count = count + 1

        obj.write({"crawl_status": "content_crawl",
                   "content_ids": content})



