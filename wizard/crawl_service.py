from odoo import models, fields, api


class CrawlService(models.Model):
    _name = "crawl.service"
    _description = "Crawl Service"

    name = fields.Char(string="Name")

    def trigger_freesexkahani(self):
        obj = self.env["free.sex.kahani"].create({"domain": "https://www.freesexkahani.com/",
                                                  "url": "https://www.freesexkahani.com/",
                                                  "page": 10})

        obj.trigger_update_story()



