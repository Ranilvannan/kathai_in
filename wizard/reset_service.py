from odoo import models, fields, api, exceptions


PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2")]


class ResetService(models.TransientModel):
    _name = "reset.service"
    _description = "Reset Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_export_reset(self):
        if self.project == "project_site1":
            self.site_reset("project.site1")

    def site_reset(self, site_model):
        un_exported = self.env[site_model].search_count([("is_exported", "=", False)])

        if un_exported:
            raise exceptions.ValidationError("Error! Reset needs all records to be exported")

        recs = self.env[site_model].search([])

        for rec in recs:
            rec.is_exported = False
