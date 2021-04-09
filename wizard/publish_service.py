from odoo import models, fields, api, exceptions

PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2")]


class PublishService(models.TransientModel):
    _name = "publish.service"
    _description = "Publish Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)
    count = fields.Integer(string="No. of Records", required=1)
    date = fields.Date(string="Date", required=1)

    def trigger_publish(self):
        if self.project == "project_site1":
            self.project_site_publish("project.site1")

    def project_site_publish(self, site_model):
        recs = self.env[site_model].search([("published_on", "=", False)])[:self.count]

        for rec in recs:
            rec.published_on = self.date
