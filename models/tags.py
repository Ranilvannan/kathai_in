from odoo import models, fields


class KathaiAduTags(models.Model):
    _name = "kathai.adu.tags"
    _description = "Story Tags"
    _rec_name = "name"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
