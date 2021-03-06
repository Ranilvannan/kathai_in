from odoo import models, fields, api


class CrawlService(models.Model):
    _name = "crawl.service"
    _description = "Crawl Service"

    name = fields.Char(string="Name")

    def trigger_freesexkahani_url_crawl(self):
        obj = self.env["free.sex.kahani"].create({
            "domain": "https://www.freesexkahani.com",
            "url": "https://www.freesexkahani.com",
            "page": 10})

        obj.trigger_url_crawl()

    def trigger_freesexkahani_translate(self):
        recs = self.env["story.book"].search([("crawl_domain", "=", "https://www.freesexkahani.com"),
                                              ("crawl_status", "=", "url_crawl"),
                                              ("is_translated", "=", False)])[:10]

        for rec in recs:
            rec.trigger_translate()
            rec.generate_site_url()

    def trigger_freesexkahani_content_crawl(self):
        recs = self.env["story.book"].search([("crawl_domain", "=", "https://www.freesexkahani.com"),
                                              ("crawl_status", "=", "url_crawl"),
                                              ("is_translated", "=", True)])[:10]

        for rec in recs:
            obj = self.env["free.sex.kahani"].create({"url": rec.crawl_url})
            obj.trigger_content_crawl(rec)
