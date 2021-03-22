from odoo import models, fields, exceptions


class StoryTags(models.Model):
    _name = "story.tags"
    _description = "Story Tags"
    _rec_name = "name"

    name = fields.Char(string="Name")
    title = fields.Char(string="Title")
    url = fields.Char(string="URL")
