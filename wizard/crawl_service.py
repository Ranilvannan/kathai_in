from odoo import models, fields, api


class CrawlService(models.Model):
    _name = "crawl.service"
    _description = "Crawl Service"

    name = fields.Char(string="Name")

    def trigger_freesexkahani_url_crawl(self):
        obj = self.env["free.sex.kahani"].create({
            "domain": "https://www.freesexkahani.com",
            "url": "https://www.freesexkahani.com",
            "page": 3})

        obj.trigger_url_crawl()

    def trigger_freesexkahani_content_crawl(self):
        recs = self.env["kathai.in.story"].search([("domain", "=", "https://www.freesexkahani.com"),
                                                   ("crawl_status", "=", "url_crawl")])[:2]

        for rec in recs:
            obj = self.env["free.sex.kahani"].create({"url": rec.url})
            obj.trigger_content_crawl()


