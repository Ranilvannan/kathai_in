from odoo import models, fields, api

STATUS = [("draft", "Draft"),
          ("url_crawl", "URL Crawl"),
          ("content_crawl", "Content Crawl")]


class StoryBook(models.Model):
    _name = "story.book"
    _description = "Story Book"
    _rec_name = "sequence"

    sequence = fields.Char(string="Sequence", readonly=True)

    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="story.content", inverse_name="story_id")

    domain = fields.Char(string="Domain")
    url = fields.Text(string="URL")
    parent_id = fields.Many2one(comodel_name="story.book", string="Parent")

    tag_ids = fields.Many2many(comodel_name="story.tags")
    status = fields.Selection(selection=STATUS, default=STATUS[0][0])
    is_exported = fields.Boolean(string="Is Exported", default=False)

    @api.model_create_multi
    def create(self, vals):
        vals["sequence"] = self.env['ir.sequence'].next_by_code(self._name)
        return super(StoryBook, self).create(vals)


class StoryContent(models.Model):
    _name = "story.content"
    _description = "Story Content"

    order_seq = fields.Integer(string="Order Sequence")
    paragraph = fields.Text(string="Paragraph")
    story_id = fields.Many2one(comodel_name="story.book", string="Story")

