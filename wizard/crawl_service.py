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
        recs = self.env["kathai.in.story"].search([("domain", "=", "https://www.freesexkahani.com"),
                                                   ("crawl_status", "=", "url_crawl")])[:10]

        for rec in recs:
            obj = self.env["free.sex.kahani"].create({"url": rec.url})
            obj.trigger_content_crawl()

    def trigger_set_parent_id(self):
        recs = self.env["kathai.in.story"].search([("crawl_status", "=", "content_crawl"),
                                                   ("parent_url", "!=", False),
                                                   ("parent_id", "=", False)])

        print(recs, "====")
        for rec in recs:
            obj = self.env["kathai.in.story"].search([("url", "=", rec.parent_url)])
            print(obj)
            if obj:
                rec.parent_id = obj.id

