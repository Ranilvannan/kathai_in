from odoo import models, fields, api, exceptions


PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2")]


class SitemapService(models.TransientModel):
    _name = "sitemap.service"
    _description = "Sitemap Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_sitemap(self):
        if self.project == "project_site1":
            pass

