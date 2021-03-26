from odoo import models, fields, api
from datetime import datetime

MONTH = [("1", "January")]
YEAR = [("2021", "2021"), ("2022", "2022")]


class SitemapService(models.TransientModel):
    _name = "sitemap.service"
    _description = "Sitemap Service"

    month = fields.Selection(selection=MONTH, string="Months")
    year = fields.Selection(selection=YEAR, string="Year")

    def trigger_monthly_sitemap(self):
        pass

    def trigger_page_wise_sitemap(self):
        pass
