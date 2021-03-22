from odoo import models, fields


class StoryCategory(models.Model):
    _name = "story.category"
    _description = "Story Category"
    _rec_name = "name"

    name = fields.Char(string="Name")
    url = fields.Char(string="URL")
