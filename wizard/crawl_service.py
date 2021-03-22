from odoo import models, fields, api


class CrawlService(models.Model):
    _name = "crawl.service"
    _description = "Crawl Service"

    name = fields.Char(string="Name")

    def trigger_freesexkahani_crawl(self):
        obj = self.env["free.sex.kahani"].create({
            "domain": "https://www.freesexkahani.com",
            "url": "https://www.freesexkahani.com",
            "page": 2})

        obj.trigger_crawl()

    def trigger_desitales2_crawl(self):
        obj = self.env["desi.tales2"].create({
            "domain": "https://www.desitales2.com",
            "url": "https://www.desitales2.com",
            "page": 2})

        obj.trigger_crawl()

