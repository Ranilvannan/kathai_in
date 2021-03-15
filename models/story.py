from odoo import models, fields, api, exceptions
from datetime import datetime

import string
import random


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
    language = fields.Many2one(comodel_name="story.language")

    # SITE INFO
    site_url = fields.Text(string="URL")
    site_title = fields.Text(string="Title")
    site_preview = fields.Text(string="Preview")
    tag_ids = fields.Many2many(comodel_name="story.tags")
    parent_id = fields.Many2one(comodel_name="story.book")
    date_of_publish = fields.Date(string="Date Of Publish")
    active = fields.Boolean(string="Active", default=True)

    # CONTENT
    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="story.content", inverse_name="story_id")

    # Service
    is_url_crawled = fields.Boolean(string="URL Crawl", default=False)
    is_content_crawled = fields.Boolean(string="Content Crawl", default=False)
    is_parent_mapped = fields.Boolean(string="Parent Mapped", default=False)
    is_exported = fields.Boolean(string="Exported", default=False)
    is_published = fields.Boolean(string="Published", default=False)

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
        else:
            parent_published = True

        if site_url and content and parent and parent_published:
            result = True
        print(site_url, content, parent, parent_published)
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

