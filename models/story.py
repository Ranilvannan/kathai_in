from odoo import models, fields, api

STATUS = [("draft", "Draft"),
          ("url_crawl", "URL Crawl"),
          ("content_crawl", "Content Crawl")]


class KathaiAduStory(models.Model):
    _name = "kathai.adu.story"
    _description = "Story Book"
    _rec_name = "sequence"

    sequence = fields.Char(string="Sequence", readonly=True)

    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="kathai.adu.content", inverse_name="story_id")

    domain = fields.Char(string="Domain")
    url = fields.Text(string="URL")
    parent_id = fields.Many2one(comodel_name="kathai.adu.story", string="Parent")

    tag_ids = fields.Many2many(comodel_name="kathai.adu.tags")
    status = fields.Selection(selection=STATUS, default=STATUS[0][0])
    is_exported = fields.Boolean(string="Is Exported", default=False)

    @api.model
    def create(self, vals):
        vals["sequence"] = self.env['ir.sequence'].next_by_code("kathai.adu.story")
        return super(KathaiAduStory, self).create(vals)


class KathaiAduContent(models.Model):
    _name = "kathai.adu.content"
    _description = "Story Content"

    order_seq = fields.Integer(string="Order Sequence")
    paragraph = fields.Text(string="Paragraph")
    story_id = fields.Many2one(comodel_name="kathai.adu.story", string="Story")

