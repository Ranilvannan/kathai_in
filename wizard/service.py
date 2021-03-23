from odoo import models, fields


class Service(models.Model):
    _name = "service.service"
    _description = "Service Service"

    def trigger_crawl(self):
        self.env["crawl.service"].trigger_desitales2_crawl()

