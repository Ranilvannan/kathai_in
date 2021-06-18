from odoo import models, fields, api, exceptions
from datetime import datetime

PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2"),
           ("project_site3", "Project Site 3"),
           ("project_site4", "Project Site 4"),
           ("project_site5", "Project Site 5"),
           ("project_site6", "Project Site 6"),
           ("project_site7", "Project Site 7")]


class TransferService(models.TransientModel):
    _name = "transfer.service"
    _description = "Transfer Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_transfer(self):
        if self.project == "project_site1":
            self.project_site1_transfer()
        elif self.project == "project_site2":
            self.project_site2_transfer()
        elif self.project == "project_site3":
            self.project_site3_transfer()
        elif self.project == "project_site4":
            self.project_site4_transfer()
        elif self.project == "project_site5":
            self.project_site5_transfer()
        elif self.project == "project_site6":
            self.project_site6_transfer()
        elif self.project == "project_site7":
            self.project_site7_transfer()

    def project_site1_transfer(self):
        site_model = "project.site1"
        book_field = "project_site1"
        lang = "English"
        self.next_record_import(site_model, book_field)
        self.new_record_import(site_model, book_field, lang)

    def project_site2_transfer(self):
        site_model = "project.site2"
        book_field = "project_site2"
        lang = "Tamil"
        self.next_record_import(site_model, book_field)
        self.new_record_import(site_model, book_field, lang)

    def project_site3_transfer(self):
        site_model = "project.site3"
        book_field = "project_site3"
        lang = "Hindi"
        self.next_record_import(site_model, book_field)
        self.new_record_import(site_model, book_field, lang)

    def project_site4_transfer(self):
        site_model = "project.site4"
        book_field = "project_site4"
        lang = "Malayalam"
        self.next_record_import(site_model, book_field)
        self.new_record_import(site_model, book_field, lang)

    def project_site5_transfer(self):
        site_model = "project.site5"
        book_field = "project_site5"
        lang = "Telugu"
        self.next_record_import(site_model, book_field)
        self.new_record_import(site_model, book_field, lang)

    def project_site6_transfer(self):
        site_model = "project.site6"
        book_field = "project_site6"
        lang = "Bengali"
        self.next_record_import(site_model, book_field)
        self.new_record_import(site_model, book_field, lang)

    def project_site7_transfer(self):
        site_model = "project.site7"
        book_field = "project_site7"
        lang = "Kannada"
        self.next_record_import(site_model, book_field)
        self.new_record_import(site_model, book_field, lang)

    def new_record_import(self, site_model, book_field, lang):
        recs = self.env["story.book"].search([(book_field, "=", False),
                                              ("language.name", "=", lang),
                                              ("prev_url", "=", False)])[:10]

        for rec in recs:
            category_obj = self.env["category.tag"].search([("name", "=", rec.category),
                                                            ("language", "=", rec.language.id),
                                                            ("category_id", "!=", False)])

            if category_obj:
                data = {"title": rec.title,
                        "preview": rec.preview,
                        "ref": rec.name,
                        "category_id": category_obj.category_id.id,
                        "language": rec.language.id,
                        "content": rec.content}
                record_id = self.env[site_model].create(data)
                rec.write({book_field: record_id.name})

    def next_record_import(self, site_model, book_field):
        recs = self.env[site_model].search([("last_checked_on", "!=", datetime.now()),
                                            ("is_exported", "=", True),
                                            ("next_id", "=", False)])[:10]

        for rec in recs:
            story_id = self.env["story.book"].search([("name", "=", rec.ref)])
            if story_id:
                story_obj = self.env["story.book"].search([("prev_url", "=", story_id.crawl_url),
                                                           (book_field, "=", False)])
                if story_obj:
                    category_obj = self.env["category.tag"].search([("name", "=", story_obj.category),
                                                                    ("language", "=", rec.language.id),
                                                                    ("category_id", "!=", False)])
                    if category_obj:
                        data = {"title": story_obj.title,
                                "preview": story_obj.preview,
                                "ref": story_obj.name,
                                "category_id": category_obj.category_id.id,
                                "prev_id": rec.id,
                                "language": rec.language.id,
                                "content": rec.content}

                        record_id = self.env[site_model].create(data)
                        rec.write({"next_id": record_id.id})
                        story_obj.write({book_field: record_id.name})

            rec.write({"last_checked_on": datetime.now()})


