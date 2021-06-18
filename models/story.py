from odoo import models, fields, api, exceptions
from datetime import datetime
import random
import string


class StoryBook(models.Model):
    _name = "story.book"
    _description = "Story Book"
    _rec_name = "name"
    _order = "sequence"

    sequence = fields.Char(string="Sequence", readonly=True)
    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", default=datetime.now())

    # CRAWL INFO
    crawl_domain = fields.Char(string="Domain")
    crawl_url = fields.Text(string="URL")
    prev_url = fields.Text(string="Previous URL")
    language = fields.Many2one(comodel_name="story.language", string="Language")

    # CONTENT
    title = fields.Text(string="Title")
    content = fields.Text(string="Content")
    category = fields.Char(string="Category")

    # Status
    active = fields.Boolean(string="Active", default=True)
    project_site1 = fields.Char(string="Project Site 1")
    project_site2 = fields.Char(string="Project Site 2")
    project_site3 = fields.Char(string="Project Site 3")
    project_site4 = fields.Char(string="Project Site 4")
    project_site5 = fields.Char(string="Project Site 5")
    project_site6 = fields.Char(string="Project Site 6")
    project_site7 = fields.Char(string="Project Site 7")
    is_cat_checked = fields.Boolean(string="Is Category Checked", default=False)

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("story.book")
        vals["sequence"] = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
        return super(StoryBook, self).create(vals)
