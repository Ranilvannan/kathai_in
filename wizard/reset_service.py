from odoo import models, fields, api, exceptions


PROJECT = [("project.site1", "Project Site 1"),
           ("project.site2", "Project Site 2")]


class ResetService(models.TransientModel):
    _name = "reset.service"
    _description = "Reset Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def export_reset(self):
        obj = self.env[self.project]
        un_exported = obj.search_count([("is_exported", "=", False)])
        if un_exported:
            raise exceptions.ValidationError("Error! Reset needs all records to be exported")

        recs = obj.search([])

        for rec in recs:
            rec.is_exported = False
