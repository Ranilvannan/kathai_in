from odoo import models, fields, exceptions


class History(models.Model):
    _name = "history.history"
    _description = "History"
    _rec_name = "domain"

    domain = fields.Char(string="Domain")
    url = fields.Char(string="URL")
