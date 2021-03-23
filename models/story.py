from odoo import models, fields, api, exceptions
from datetime import datetime


class StoryBook(models.Model):
    _name = "story.book"
    _description = "Story Book"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", default=datetime.now())

    # CRAWL INFO
    crawl_domain = fields.Char(string="Domain")
    crawl_url = fields.Text(string="URL")
    prev_url = fields.Text(string="Previous URL")
    language = fields.Many2one(comodel_name="story.language")

    # CONTENT
    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="story.content", inverse_name="story_id")
    category = fields.Char(string="Category")

    # Status
    active = fields.Boolean(string="Active", default=True)
    project_site1 = fields.Char(string="Project Site 1")

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

