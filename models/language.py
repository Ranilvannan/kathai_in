from odoo import models, fields, exceptions


class StoryLanguage(models.Model):
    _name = "story.language"
    _description = "Story Language"
    _rec_name = "name"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
