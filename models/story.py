from odoo import models, fields, api, exceptions
from datetime import datetime
from googletrans import Translator
import string
import random

CRAWL_STATUS = [("url_crawl", "URL Crawl"), ("content_crawl", "Content Crawl")]


class StoryBook(models.Model):
    _name = "story.book"
    _description = "Story Book"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", default=datetime.now())

    # CRAWL INFO
    crawl_domain = fields.Char(string="Domain")
    crawl_url = fields.Text(string="URL")
    parent_url = fields.Text(string="Parent URL")
    crawl_status = fields.Selection(selection=CRAWL_STATUS, string="Crawl Status")
    language = fields.Many2one(comodel_name="story.language")

    # SITE INFO
    site_url = fields.Text(string="URL")
    site_title = fields.Text(string="Title")
    site_preview = fields.Text(string="Preview")
    tag_ids = fields.Many2many(comodel_name="story.tags")
    parent_id = fields.Many2one(comodel_name="story.book")
    has_published = fields.Boolean(string="Has Published", default=False)
    is_exported = fields.Boolean(string="Is Exported", default=False)
    is_translated = fields.Boolean(string="Is Translated", default=False)
    date_of_publish = fields.Date(string="Date Of Publish")
    active = fields.Boolean(string="Active", default=True)

    # CONTENT
    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="story.content", inverse_name="story_id")

    def trigger_deactive(self):
        self.active = False

    def trigger_translate(self):
        translator = Translator()
        title = translator.translate(self.title)
        preview = translator.translate(self.preview)

        self.write({"site_title": title.text,
                    "site_preview": preview.text,
                    "is_translated": True})

    def generate_site_url(self):
        site_url = self.site_title
        new_site_url = site_url.lower()
        new_site_url = new_site_url.replace(" ", "-")
        new_site_url = new_site_url.replace("'", "")
        new_site_url = new_site_url.replace(",", "")

        res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
        self.site_url = "{0}-{1}".format(new_site_url, res)

    def check_publish(self):
        result = False
        site_url = False
        content = False
        parent = False
        parent_published = False

        if self.site_url:
            site_url = True

        if self.content_ids:
            content = True

        if self.parent_url and self.parent_id:
            parent = True
        elif (not self.parent_url) and (not self.parent_id):
            parent = True

        if self.parent_id:
            if self.parent_id.has_published:
                parent_published = True

        if site_url and content and parent and parent_published:
            result = True

        return result

    def trigger_publish(self):
        publish = self.check_publish()

        if publish:
            self.write({"date_of_publish": datetime.now(),
                        "has_published": True})

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("story.book")
        return super(StoryBook, self).create(vals)


class StoryContent(models.Model):
    _name = "story.content"
    _description = "Story Content"

    order_seq = fields.Integer(string="Order Sequence")
    content = fields.Text(string="Content")
    story_id = fields.Many2one(comodel_name="story.book", string="Story")

