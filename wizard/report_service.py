from odoo import models, fields, api, exceptions

PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2"),
           ("project_site3", "Project Site 3"),
           ("project_site4", "Project Site 4")]


class ReportService(models.TransientModel):
    _name = "report.service"
    _description = "Report Service"

    project = fields.Selection(selection=PROJECT, string="Project")
