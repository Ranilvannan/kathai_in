from odoo import models, fields, api, exceptions


PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2"),
           ("project_site3", "Project Site 3"),
           ("project_site4", "Project Site 4"),
           ("project_site5", "Project Site 5"),
           ("project_site6", "Project Site 6"),
           ("project_site7", "Project Site 7")]


class ControlService(models.TransientModel):
    _name = "control.service"
    _description = "Control Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_generate_tag(self):
        self.env["category.tag"].trigger_generate_tag()

    def trigger_transfer_service(self):
        rec = self.env["transfer.service"].create({"project": self.project})
        rec.trigger_transfer()

    def trigger_story_export(self):
        rec = self.env["export.service"].create({"project": self.project})
        rec.trigger_story_export()

    def trigger_category_export(self):
        rec = self.env["export.service"].create({"project": self.project})
        rec.trigger_category_export()

    def trigger_gallery_export(self):
        rec = self.env["export.service"].create({"project": self.project})
        rec.trigger_gallery_export()

    def trigger_history_crawl(self):
        site = "desitales2"
        crawl_type = "history"

        obj = self.env["crawl.service"].create({"site": site, "crawl_type": crawl_type})
        obj.trigger_crawl()

        site = "tamilkamaveri"
        crawl_type = "history"

        obj = self.env["crawl.service"].create({"site": site, "crawl_type": crawl_type})
        obj.trigger_crawl()

        site = "antarvasnax"
        crawl_type = "history"

        obj = self.env["crawl.service"].create({"site": site, "crawl_type": crawl_type})
        obj.trigger_crawl()

        site = "kambimalayalamkathakal"
        crawl_type = "history"

        obj = self.env["crawl.service"].create({"site": site, "crawl_type": crawl_type})
        obj.trigger_crawl()

