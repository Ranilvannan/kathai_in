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

    def trigger_site_data_update(self):
        self.env["project.site1"].trigger_site_data()

    def trigger_site_validate(self):
        self.env["project.site1"].trigger_check_valid()
