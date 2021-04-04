from odoo import models, fields, api, exceptions
from odoo.tools import config
from datetime import datetime
import random

MIN_PUBLISH = 50
NUM_SELECT = 2
PROJECT = [("project.site1", "Project Site 1"),
           ("project.site2", "Project Site 2")]


class TransferService(models.TransientModel):
    _name = "transfer.service"
    _description = "Transfer Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_transfer(self):
        if self.project == "project.site1":
            self.project_site1_transfer()

    def project_site1_transfer(self):
        site_model = "project.site1"
        book_field = "project_site1"
        lang = "English"
        self.next_record_import(site_model, book_field)
        self.new_record_import(site_model, book_field, lang)

    def new_record_import(self, site_model, book_field, lang):
        list_of_random_items = []
        recs = self.env["story.book"].search([(book_field, "=", False),
                                              ("language.name", "=", lang),
                                              ("prev_url", "=", False)])

        if len(recs) > NUM_SELECT:
            list_of_random_items = random.sample(recs, NUM_SELECT)

        for rec in list_of_random_items:
            publish = self.env[site_model].search_count([("date", "=", datetime.now())])
            category_obj = self.env["category.tag"].search([("name", "=", rec.category),
                                                            ("category_id", "!=", False)])

            if category_obj and (publish < MIN_PUBLISH):
                data = {"title": rec.title,
                        "preview": rec.preview,
                        "ref": rec.name,
                        "category_id": category_obj.category_id.id,
                        "content_ids": [(0, 0, {"order_seq": item.order_seq,
                                                "content": item.content})
                                        for item in rec.content_ids]}

                record_id = self.env[site_model].create(data)
                rec.write({book_field: record_id.name})

    def next_record_import(self, site_model, book_field):
        recs = self.env[site_model].search([("last_checked_on", "!=", datetime.now()),
                                            ("is_exported", "=", True),
                                            ("next_id", "=", False)])[:100]

        for rec in recs:
            story_id = self.env["story.book"].search([("name", "=", rec.ref)])
            if story_id:
                story_obj = self.env["story.book"].search([("prev_url", "=", story_id.crawl_url),
                                                           (book_field, "=", False)])
                if story_obj:
                    publish = self.env[site_model].search_count([("date", "=", datetime.now())])
                    category_obj = self.env["category.tag"].search([("name", "=", story_obj.category),
                                                                    ("category_id", "!=", False)])
                    if category_obj and (publish < MIN_PUBLISH):
                        data = {"title": story_obj.title,
                                "preview": story_obj.preview,
                                "ref": story_obj.name,
                                "category_id": category_obj.category_id.id,
                                "prev_id": rec.id,
                                "content_ids": [(0, 0, {"order_seq": item.order_seq,
                                                        "content": item.content})
                                                for item in story_obj.content_ids]}

                        record_id = self.env[site_model].create(data)
                        rec.write({"next_id": record_id.id})
                        story_obj.write({book_field: record_id.name})

            rec.write({"last_checked_on": datetime.now()})


