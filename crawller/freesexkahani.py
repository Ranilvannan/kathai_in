from odoo import models, fields, api
from .common import get_url_content, clean_url


class FreeSexKahani(models.TransientModel):
    _name = "free.sex.kahani"
    _description = "Free Sex Kahani"

    domain = fields.Char(string="Domain")
    url = fields.Text(string="URL")
    page = fields.Integer(string="Page Numbers")

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
                language = self.env["story.language"].search([("code", "=", "HINDI")])
                site_title = translate_text(title)
                site_preview = translate_text(preview)
                site_url = generate_url(site_title)

                content_html = get_url_content(url)
                parent_url = self.article_parent(content_html, url)

                data = {"title": title,
                        "preview": preview,
                        "site_url": site_url,
                        "site_title": site_title,
                        "site_preview": site_preview,
                        "crawl_domain": self.domain,
                        "crawl_url": url,
                        "parent_url": parent_url,
                        "tag_ids": [(6, 0, [tag_id])],
                        "language": language.id,
                        "content_ids": self.content_crawl(content_html)}

                self.env["story.book"].create(data)

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

    def trigger_crawl(self):
        for i in range(self.page):
            article_html = get_url_content(self.url)
            self.get_next_page(article_html)
            self.create_article(article_html)

    def content_crawl(self, soup):
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

    def article_parent(self, soup, current_url):
        url = None
        prev_url = self.content_previous_url(soup)

        if prev_url:
            previous_page_html = get_url_content(prev_url)
            next_url = self.content_next_url(previous_page_html)

            if next_url and (next_url == current_url):
                url = prev_url

        return url

    def content_previous_url(self, soup):
        parent_url = None
        content = soup.find("div", class_="entry-content")

        if content:
            parent_url_tag = content.find("a")
            if parent_url_tag:
                parent_url = parent_url_tag["href"]
                parent_url = clean_url(parent_url)

        return parent_url

    def content_next_url(self, soup):
        next_url = None
        content = soup.find("div", class_="entry-content")

        if content:
            links = content.find_all("a")
            if links:
                next_url = links[-1]["href"]
                next_url = clean_url(next_url)

        return next_url




