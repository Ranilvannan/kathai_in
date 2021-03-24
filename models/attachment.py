from odoo import models, fields


class Attachment(models.Model):
    _name = "book.attachment"
    _description = "Attachment"

    name = fields.Char(string="name")
    description = fields.Char(string="Description")
    att = fields.Binary(string="Attachment")
