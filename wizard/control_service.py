from odoo import models, fields, api, exceptions


PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2")]


class ControlService(models.TransientModel):
    _name = "control.service"
    _description = "Control Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def get_project(self):
        result = None
        if self.project == "project_site1":
            result = "project.site1"

        return result

    def trigger_transfer_service(self):
        site_model = self.get_project()
        rec = self.env["transfer.service"].create({"name": self.project})
        rec.trigger_transfer()

