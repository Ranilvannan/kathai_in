from odoo import models, fields, api, exceptions

PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2"),
           ("project_site3", "Project Site 3"),
           ("project_site4", "Project Site 4"),
           ("project_site5", "Project Site 5"),
           ("project_site6", "Project Site 6"),
           ("project_site7", "Project Site 7")]


class PublishService(models.TransientModel):
    _name = "publish.service"
    _description = "Publish Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)
    count = fields.Integer(string="No. of Records", required=1)
    date = fields.Date(string="Date", required=1)

    def trigger_publish(self):
        if self.project == "project_site1":
            self.project_site_publish("project.site1")
        elif self.project == "project_site2":
            self.project_site_publish("project.site2")
        elif self.project == "project_site3":
            self.project_site_publish("project.site3")
        elif self.project == "project_site4":
            self.project_site_publish("project.site4")
        elif self.project == "project_site5":
            self.project_site_publish("project.site5")
        elif self.project == "project_site6":
            self.project_site_publish("project.site6")
        elif self.project == "project_site7":
            self.project_site_publish("project.site7")

    def project_site_publish(self, site_model):
        recs = self.env[site_model].search([("is_valid", "=", True), ("published_on", "=", False)])[:self.count]

        for rec in recs:
            rec.published_on = self.date
