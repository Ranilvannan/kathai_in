from odoo import models, fields


class StoryTags(models.Model):
    _name = "story.tags"
    _description = "Story Tags"
    _rec_name = "name"

    name = fields.Char(string="Name")
