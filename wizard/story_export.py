from odoo import models, fields


class StoryExport(models.TransientModel):
    _name = "story.export"
    _description = "Story Export"

    name = fields.Char(string="Name")

    def trigger_export(self):
        pass
