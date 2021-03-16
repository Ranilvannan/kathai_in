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

    # Status
    is_exported = fields.Boolean(string="Exported", default=False)
    has_published = fields.Boolean(string="Published", default=False)

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

