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

    # CONTENT
    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="story.content", inverse_name="story_id")

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

    def check_content_crawl(self):
        if self.crawl_status != "content_crawl":
            raise exceptions.ValidationError("Error! Story must be publish after CONTENT CRAWL")

    def check_parent_url(self):
        if self.parent_url and (not self.parent_id):
            obj = self.env["story.book"].search([("crawl_url", "=", self.parent_url)])
            if obj:
                self.parent_id = obj.id
            else:
                raise exceptions.ValidationError("Error! Parent not found")

    def check_site_url(self):
        if not self.site_url:
            raise exceptions.ValidationError("Error! Site URL not found")

    def trigger_publish(self):
        self.check_content_crawl()
        self.check_parent_url()
        self.check_parent_url()
        parent_status = self.parent_url_status()

        if parent_status:
            self.publish_parent_url()

    def parent_url_status(self):
        recs = self.env["story.book"].search([("parent_id", "child_of", self.parent_id.id)])

        result = True
        for rec in recs:
            if not rec.crawl_url == "content_crawl":
                result = False

        return result

    def publish_parent_url(self):
        recs = self.env["story.book"].search([("parent_id", "child_of", self.parent_id.id)])
        for rec in recs:
            if not rec.has_published:
                rec.write({"date_of_publish": datetime.now(),
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

