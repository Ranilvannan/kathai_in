from odoo import models, fields
from .common import get_url_content, clean_url


class KambimalayalamKathakal(models.TransientModel):
    _name = "kambimalayalam.kathakal"
    _description = "kambimalayalamkathakal"

    domain = fields.Char(string="Domain")
    url = fields.Text(string="URL")
    page = fields.Integer(string="Page Numbers")

    def article_title(self, article):
        result = None
        title_tag = article.find("h2")

        if title_tag:
            a_tag = title_tag.find("a")
            if a_tag:
                result = a_tag.text.strip()

        return result

    def article_preview(self, article):
        result = None
        paragraph_tag = article.find("p", class_="exceprt")

        if paragraph_tag:
            result = paragraph_tag.text.strip()

        return result

    def article_url(self, article):
        result = None
        title_tag = article.find("h2")

        if title_tag:
            a_tag = title_tag.find("a")
            if a_tag:
                result = clean_url(a_tag["href"])

        return result

    def article_category(self, article):
        result = "Others"
        category = article.find("span", class_="meta-category")
        if category:
            category_link = category.find("a")
            if category_link:
                result = category_link.text.strip()

        return result

    def create_article(self, soup):
        article_list = soup.find_all("article")

        for article in article_list:
            url = self.article_url(article)
            rec = self.env["story.book"].search([("crawl_url", "=", url)])

            if not rec:
                title = self.article_title(article)
                category = self.article_category(article)
                language = self.env["story.language"].search([("code", "=", "MALAYALAM")])

                content_html = get_url_content(url)
                prev_url = self.article_previous(content_html)

                data = {
                    "title": title,
                    "content": self.content_crawl(content_html),
                    "crawl_domain": self.domain,
                    "crawl_url": url,
                    "prev_url": prev_url,
                    "language": language.id,
                    "category": category
                        }

                self.env["story.book"].create(data)

    def get_next_page(self, soup):
        next_page_list = soup.find_all("a", class_="next page-numbers")

        if next_page_list:
            next_page = next_page_list[0]
            self.url = clean_url(next_page["href"])

            # Removed If history not needed
            history_obj = self.env["history.history"].search([("domain", "=", self.domain)])
            if history_obj:
                history_obj.url = self.url
            else:
                self.env["history.history"].create({"domain": self.domain, "url": self.url})

    def trigger_crawl(self):
        for i in range(self.page):
            article_html = get_url_content(self.url)
            self.get_next_page(article_html)
            self.create_article(article_html)

    def content_crawl(self, soup):
        content_data = ""
        content = soup.find("section", class_="story-content")

        if content:
            recs = content.find_all("p")
            content_list = [rec.text.strip() for rec in recs]
            content_data = "|#|".join(content_list)

        return content_data

    def article_previous(self, soup):
        url = None
        h4_tags = soup.find_all("h4")
        for h4_tag in h4_tags:
            i_tag = h4_tag.find("i")
            if i_tag:
                i_tag_text = i_tag.text.strip()
                if i_tag_text == "keyboard_arrow_left":
                    url_tag = h4_tag.find("a")
                    if url_tag:
                        url = clean_url(url_tag["href"])

        return url






