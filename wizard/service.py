from odoo import models, fields


class Service(models.Model):
    _name = "service.service"
    _description = "Service Service"

    def trigger_crawl(self):
        self.env["crawl.service"].trigger_desitales2_crawl()

    def trigger_category_tag_update(self):
        self.env["category.tag"].trigger_generate_tag()

    def trigger_site1_import(self):
        self.env["project.site1"].trigger_data_import()
