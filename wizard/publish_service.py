from odoo import models, fields, api
from datetime import datetime


class PublishService(models.Model):
    _name = "publish.service"
    _description = "Publish Service"

    def trigger_publish(self):
        recs = self.env["story.language"].search([])
        for rec in recs:
            story_list = self.env["story.book"].search([("date_of_publish", "=", datetime.now()),
                                                        ("has_published", "=", True),
                                                        ("language", "=", rec.id)])

            if len(story_list) < 10:
                un_published_list = self.env["story.book"].search([("language", "=", rec.id),
                                                                   ("has_published", "=", False),
                                                                   ("valid", "=", True)])[:10]

                for article in un_published_list:
                    article.write({"has_published": True,
                                   "date_of_publish": datetime.now()})
