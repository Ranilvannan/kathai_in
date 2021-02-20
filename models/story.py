from odoo import models, fields, api, exceptions
from datetime import datetime

CRAWL_STATUS = [("url_crawl", "URL Crawl"), ("content_crawl", "Content Crawl")]
STATUS = [("draft", "Draft"), ("publish", "Publish")]


class KathaiInStory(models.Model):
    _name = "kathai.in.story"
    _description = "Story Book"
    _rec_name = "sequence"

    sequence = fields.Char(string="Sequence", readonly=True)

    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="kathai.in.content", inverse_name="story_id")

    domain = fields.Char(string="Domain")
    url = fields.Text(string="URL")
    parent_id = fields.Many2one(comodel_name="kathai.in.story", string="Parent")
    crawl_status = fields.Selection(selection=CRAWL_STATUS, string="Crawl Status")

    tag_ids = fields.Many2many(comodel_name="kathai.in.tags")
    status = fields.Selection(selection=STATUS, default=STATUS[0][0])
    is_exported = fields.Boolean(string="Is Exported", default=False)
    dop = fields.Date(string="Date Of Publishing")

    def trigger_publish(self):
        if self.crawl_status != "content_crawl":
            raise exceptions.ValidationError("Error! Story must be publish after CONTENT CRAWL")

        self.dop = datetime.now()
        self.status = "publish"

    @api.model
    def create(self, vals):
        vals["sequence"] = self.env['ir.sequence'].next_by_code("kathai.in.story")
        return super(KathaiInStory, self).create(vals)


class KathaiInContent(models.Model):
    _name = "kathai.in.content"
    _description = "Story Content"

    order_seq = fields.Integer(string="Order Sequence")
    paragraph = fields.Text(string="Paragraph")
    story_id = fields.Many2one(comodel_name="kathai.in.story", string="Story")

