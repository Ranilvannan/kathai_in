from odoo import models, fields, api
from bs4 import BeautifulSoup
import requests


class FreeSexKahaniUrlCrawl(models.TransientModel):
    _name = "free.sex.kahani.url.crawl"
    _description = "Free Sex Kahani URL Crawl"

    domain = fields.Char(string="Domain")
    url = fields.Text(string="URL")
    page = fields.Integer(string="Page Numbers")
    is_active = fields.Boolean(string="Active", default=True)

    def get_content(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup

    def get_article(self, soup):
        article_list = soup.find_all("div", class_="inside-article")

        duplicate_count = 0
        for article in article_list:
            try:
                title_tag = article.find("h2")
                title = title_tag.text

                preview_tag = article.find("div", class_="entry-content")
                preview = preview_tag.text

                url_tag = preview_tag.find("a")
                url = url_tag["href"]

                tags = article.find("span", class_="cat-links")
                tags_link = tags.find("a")
                tag = tags_link.text


                tag_id = self.check_tag(tag)

                rec = self.env["kathai.in.story"].search([("url", "=", url)])

                if rec:
                    duplicate_count = duplicate_count + 1

                else:
                    self.env["kathai.in.story"].create({"title": title,
                                                        "preview": preview,
                                                        "domain": self.domain,
                                                        "url": url,
                                                        "tag_ids": [(6, 0, [tag_id])],
                                                        "crawl_status": "url_crawl"})

                if duplicate_count >= 5:
                    self.is_active = False
            except:
                pass

    def check_tag(self, tag):
        tag_obj = self.env["kathai.in.tags"].search([("name", "=", tag)])

        if not tag_obj:
            new_tag_obj = self.env["kathai.in.tags"].create({"name": tag})
            return new_tag_obj.id

        return tag_obj.id

    def get_next_page(self, soup):
        next_page_list = soup.find_all("a", class_="next page-numbers")

        if next_page_list:
            next_page = next_page_list[0]
            self.url = next_page["href"]

    def trigger_crawl(self):
        for i in range(self.page):
            if self.is_active:
                soup = self.get_content()
                self.get_next_page(soup)
                self.get_article(soup)


