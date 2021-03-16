from odoo import models, fields, api
from .common import translate_text, clean_url, generate_url, get_url_content
from bs4 import BeautifulSoup
import requests


class FreeSexKahani(models.TransientModel):
    _name = "free.sex.kahani"
    _description = "Free Sex Kahani"

    domain = 'https://www.freesexkahani.com'
    url = 'https://www.freesexkahani.com'
    page = 2

    def article_title(self, article):
        result = None
        title_tag = article.find("h2")

        if title_tag:
            result = title_tag.text

        return result

    def article_preview(self, article):
        result = None
        preview_tag = article.find("div", class_="entry-content")

        if preview_tag:
            paragraph_tag = preview_tag.find("p")
            if paragraph_tag:
                result = paragraph_tag.text

        return result

    def article_url(self, article):
        result = None

        preview_tag = article.find("div", class_="entry-content")
        if preview_tag:
            url_tag = preview_tag.find("a")

            if url_tag:
                result = clean_url(url_tag["href"])

        return result

    def article_tags(self, article):
        result = "Others"
        tags = article.find("span", class_="cat-links")
        if tags:
            tags_link = tags.find("a")
            if tags_link:
                result = tags_link.text

        return result

    def create_article(self, soup):
        article_list = soup.find_all("div", class_="inside-article")

        for article in article_list:
            url = self.article_url(article)
            rec = self.env["story.book"].search([("crawl_url", "=", url)])

            if not rec:
                title = self.article_title(article)
                preview = self.article_preview(article)
                tag = self.article_tags(article)
                tag_id = self.check_tag(tag)

                data = {"title": title,
                        "preview": preview,
                        "site_title": translate_text(title),
                        "site_preview": translate_text(preview),
                        "crawl_domain": self.domain,
                        "crawl_url": url,
                        "tag_ids": [(6, 0, [tag_id])],
                        "language": self.get_language(),
                        "content_ids": self.content_crawl(url)}

                self.env["story.book"].create(data)

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
            soup = get_url_content(self.url)
            self.get_next_page(soup)
            self.create_article(soup)

    def content_crawl(self, url):
        soup = get_url_content(url)
        content_list = []
        count = 1
        content = soup.find("div", class_="entry-content")

        if content:
            recs = content.find_all("p")

            for rec in recs:
                if recs[-1] == rec:
                    if rec.find("a"):
                        break
                content_list.append((0, 0, {"order_seq": count, "content": rec.text}))
                count = count + 1

        return content_list





