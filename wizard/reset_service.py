from odoo import models, fields, api, exceptions


PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2"),
           ("project_site3", "Project Site 3"),
           ("project_site4", "Project Site 4"),
           ("project_site5", "Project Site 5"),
           ("project_site6", "Project Site 6"),
           ("project_site7", "Project Site 7")]


class ResetService(models.TransientModel):
    _name = "reset.service"
    _description = "Reset Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_export_reset(self):
        if self.project == "project_site1":
            self.site_reset("project.site1")
        elif self.project == "project_site2":
            self.site_reset("project.site2")
        elif self.project == "project_site3":
            self.site_reset("project.site3")
        elif self.project == "project_site4":
            self.site_reset("project.site4")
        elif self.project == "project_site5":
            self.site_reset("project.site5")
        elif self.project == "project_site6":
            self.site_reset("project.site6")
        elif self.project == "project_site7":
            self.site_reset("project.site7")

    def site_reset(self, site_model):
        un_exported = self.env[site_model].search_count([("is_exported", "=", False)])

        if un_exported:
            raise exceptions.ValidationError("Error! Reset needs all records to be exported")

        recs = self.env[site_model].search([])

        for rec in recs:
            rec.is_exported = False
