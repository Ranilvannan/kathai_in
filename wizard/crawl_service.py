from odoo import models, fields, api


class CrawlService(models.Model):
    _name = "crawl.service"
    _description = "Crawl Service"

    name = fields.Char(string="Name")

    def trigger_freesexkahani_url_crawl(self):
        obj = self.env["free.sex.kahani"].create({
            "domain": "https://www.freesexkahani.com",
            "url": "https://www.freesexkahani.com",
            "page": 2})

        obj.trigger_url_crawl()

    def trigger_freesexkahani_content_crawl(self):
        recs = self.env["story.book"].search([("crawl_domain", "=", "https://www.freesexkahani.com"),
                                              ("crawl_status", "=", "url_crawl")])[:10]

        for rec in recs:
            obj = self.env["free.sex.kahani"].create({"url": rec.crawl_url})
            obj.trigger_content_crawl(rec)

    def trigger_set_parent_id(self):
        recs = self.env["story.book"].search([("crawl_status", "=", "content_crawl"),
                                              ("parent_url", "!=", False),
                                              ("parent_id", "=", False)])

        for rec in recs:
            obj = self.env["story.book"].search([("crawl_url", "=", rec.parent_url)])

            if obj:
                rec.parent_id = obj.id

    def trigger_publish(self):
        recs = self.env["story.book"].search([("site_url", "!=", False),
                                              ("crawl_status", "=", "content_crawl")])[:10]

        for rec in recs:
            rec.trigger_publish()
