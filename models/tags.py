from odoo import models, fields


class KathaiInTags(models.Model):
    _name = "kathai.in.tags"
    _description = "Story Tags"
    _rec_name = "name"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
