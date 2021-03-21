from odoo import models, fields, api
from .common import translate_text, clean_url, generate_url, get_url_content


class DesiTales2(models.TransientModel):
    _name = "desi.tales2"
    _description = "Desitales2"

    domain = fields.Char(string="Domain")
    url = fields.Text(string="URL")
    page = fields.Integer(string="Page Numbers")

    def article_title(self, article):
        result = None
        title_tag = article.find("h2")

        if title_tag:
            a_tag = title_tag.find("a")
            if a_tag:
                result = a_tag.text

        return result

    def article_preview(self, article):
        result = None
        paragraph_tag = article.find("p", class_="exceprt")

        if paragraph_tag:
            result = paragraph_tag.text

        return result

    def article_url(self, article):
        result = None
        title_tag = article.find("h2")

        if title_tag:
            a_tag = title_tag.find("a")
            if a_tag:
                result = clean_url(a_tag["href"])

        return result

    def article_tags(self, article):
        result = "Others"
        tags = article.find("span", class_="meta-category")
        if tags:
            tags_link = tags.find("a")
            if tags_link:
                result = tags_link.text

        return result

    def create_article(self, soup):
        article_list = soup.find_all("article")

        for article in article_list:
            url = self.article_url(article)
            rec = self.env["story.book"].search([("crawl_url", "=", url)])

            if not rec:
                title = self.article_title(article)
                preview = self.article_preview(article)
                tag = self.article_tags(article)
                tag_id = self.check_tag(tag)
                language = self.env["story.language"].search([("code", "=", "ENGLISH")])
                site_title = title
                site_preview = preview
                site_url = generate_url(site_title)

                content_html = get_url_content(url)
                parent_url = self.article_parent(content_html)

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
        content = soup.find("section", class_="story-content")

        if content:
            recs = content.find_all("p")

            for rec in recs:
                content_list.append((0, 0, {"order_seq": count, "content": rec.text}))
                count = count + 1

        return content_list

    def article_parent(self, soup):
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






