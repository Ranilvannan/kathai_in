from odoo import models, fields, api, exceptions

PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2"),
           ("project_site3", "Project Site 3"),
           ("project_site4", "Project Site 4"),
           ("project_site5", "Project Site 5"),
           ("project_site6", "Project Site 6"),
           ("project_site7", "Project Site 7")]


class ValidationService(models.TransientModel):
    _name = "validation.service"
    _description = "Validation Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_validation(self):
        if self.project == "project_site1":
            self.project_site_validation(site_model="project.site1")
        elif self.project == "project_site2":
            self.project_site_validation(site_model="project.site2")
        elif self.project == "project_site3":
            self.project_site_validation(site_model="project.site3")
        elif self.project == "project_site4":
            self.project_site_validation(site_model="project.site4")

    def project_site_validation(self, site_model):
        recs = self.env[site_model].search([("is_valid", "=", False)])[:100]

        for rec in recs:
            if rec.title \
                    and rec.preview \
                    and rec.content \
                    and rec.category_id \
                    and rec.url:
                rec.write({"is_valid": True})
