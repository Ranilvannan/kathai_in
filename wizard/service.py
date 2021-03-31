from odoo import models, fields


class Service(models.TransientModel):
    _name = "service.service"
    _description = "Service Service"

    def trigger_desitales2_crawl(self):
        self.env["crawl.service"].trigger_desitales2_crawl()

    def trigger_desitales2_history_crawl(self):
        self.env["crawl.service"].trigger_desitales2_history_crawl()

    def trigger_book_category_tag_update(self):
        self.env["category.tag"].trigger_generate_tag()

    # Project Site 1
    def trigger_project_site1_import(self):
        self.env["project.site1"].trigger_data_import()

    def trigger_project_site1_data_update(self):
        self.env["project.site1"].trigger_site_data()

    def trigger_project_site1_validate(self):
        self.env["project.site1"].trigger_check_valid()

    def trigger_project_site1_export(self):
        self.env["project.site1"].trigger_export()

    # Project Site 2
    def trigger_project_site2_import(self):
        self.env["project.site2"].trigger_data_import()

    def trigger_project_site2_data_update(self):
        self.env["project.site2"].trigger_site_data()

    def trigger_project_site2_validate(self):
        self.env["project.site2"].trigger_check_valid()

    def trigger_project_site2_export(self):
        self.env["project.site2"].trigger_export()
