from odoo import models, fields, api
from bs4 import BeautifulSoup
import requests


class FreeSexKahani(models.TransientModel):
    _name = "free.sex.kahani"
    _description = "Free Sex Kahani"

    domain = fields.Char(string="Domain")
    url = fields.Text(string="URL")
    page = fields.Integer(string="Page Numbers")

    def get_content(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup

    def get_article_data(self, article):
        title = None
        preview = None
        url = None

        title_tag = article.find("h2")
        preview_tag = article.find("div", class_="entry-content")

        if title_tag:
            title = title_tag.text

        if preview_tag:
            paragraph_tag = preview_tag.find("p")
            if paragraph_tag:
                preview = paragraph_tag.text

            url_tag = preview_tag.find("a")

            if url_tag:
                url = url_tag["href"]

        return title, preview, url

    def get_tags_data(self, article):
        tag = "Others"
        tags = article.find("span", class_="cat-links")
        if tags:
            tags_link = tags.find("a")
            if tags_link:
                tag = tags_link.text

        return tag

    def get_article(self, soup):
        article_list = soup.find_all("div", class_="inside-article")

        for article in article_list:
            title, preview, url = self.get_article_data(article)
            tag = self.get_tags_data(article)

            tag_id = self.check_tag(tag)
            rec = self.env["story.book"].search([("crawl_url", "=", url)])

            if not rec:
                self.env["story.book"].create({"title": title,
                                               "preview": preview,
                                               "crawl_domain": self.domain,
                                               "crawl_url": self.clean_url(url),
                                               "tag_ids": [(6, 0, [tag_id])],
                                               "language": self.get_language(),
                                               "crawl_status": "url_crawl"})

    def get_language(self):
        language_id = None
        obj = self.env["story.language"].search([("code", "=", "HINDI")])
        if obj:
            language_id = obj.id
        return language_id

    def check_tag(self, tag):
        tag_obj = self.env["story.tags"].search([("name", "=", tag)])

        if not tag_obj:
            new_tag_obj = self.env["story.tags"].create({"name": tag})
            return new_tag_obj.id

        return tag_obj.id

    def get_next_page(self, soup):
        next_page_list = soup.find_all("a", class_="next page-numbers")

        if next_page_list:
            next_page = next_page_list[0]
            self.url = next_page["href"]

    def trigger_url_crawl(self):
        for i in range(self.page):
            soup = self.get_content()
            self.get_next_page(soup)
            self.get_article(soup)

    def trigger_content_crawl(self):
        obj = self.env["story.book"].search([("crawl_url", "=", self.url)])
        soup = self.get_content()
        content_list = []
        count = 1
        parent_url = None
        content = soup.find("div", class_="entry-content")

        if content:
            recs = content.find_all("p")

            parent_url_tag = content.find("a")
            if parent_url_tag:
                parent_url = parent_url_tag["href"]

            for rec in recs:
                content_list.append((0, 0, {"order_seq": count, "content": rec.text}))
                count = count + 1

            obj.write({"crawl_status": "content_crawl",
                       "parent_url": self.clean_url(parent_url),
                       "content_ids": content_list})

    def clean_url(self, url):
        new_url = None
        if url:
            new_url = url.strip()

            if new_url.find("#") != -1:
                new_url, hashed = new_url.split("#")

            if new_url[-1] == "/":
                new_url = new_url[:-1]

        return new_url





