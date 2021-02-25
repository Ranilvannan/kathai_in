from odoo import models, fields, api


class CrawlService(models.Model):
    _name = "crawl.service"
    _description = "Crawl Service"

    name = fields.Char(string="Name")

    def trigger_freesexkahani_url_crawl(self):
        obj = self.env["free.sex.kahani.url.crawl"].create({
            "domain": "https://www.freesexkahani.com/",
            "url": "https://www.freesexkahani.com/",
            "page": 1})

        obj.trigger_crawl()

    def trigger_freesexkahani_content_crawl(self):
        recs = self.env["kathai.in.story"].search([("domian", "=", "https://www.freesexkahani.com/"),
                                                   ("crawl_status", "=", "url_crawl")])

        for rec in recs:
            obj = self.env["free.sex.kahani.content.crawl"].create({"url": rec.url})
            obj.trigger_crawl()


