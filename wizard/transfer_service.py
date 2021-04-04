from odoo import models, fields, api, exceptions

PROJECT = [("project.site1", "Project Site 1"),
           ("project.site2", "Project Site 2")]


class TransferService(models.TransientModel):
    _name = "transfer.service"
    _description = "Transfer Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_validation(self):
        if self.project == "project.site1":
            self.project_site1_validation(site_model="project.site1")

    def project_site1_validation(self, site_model):
        pass
