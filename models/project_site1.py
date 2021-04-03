from odoo import models, fields, api
from odoo.tools import config
import os
from datetime import datetime
import random

MIN_PUBLISH = 50
NUM_SELECT = 2
PER_PAGE = 9
LANGUAGE = "English"

DOMAIN = config["project_site1_domain"]
HOST = config["story_book_export_host"]
USERNAME = config["story_book_export_username"]
KEY_FILENAME = config["story_book_export_public_key_filename"]
REMOTE_FILE = config["project_site1_path"]


class ProjectSite1(models.Model):
    _name = "project.site1"
    _description = "Project Site 1 sexstory.osholikes"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    ref = fields.Char(string="Reference")
    date = fields.Date(string="Date", default=datetime.now())

    site_url = fields.Text(string="Site URL")
    site_title = fields.Text(string="Site Title")
    site_preview = fields.Text(string="Site Preview")

    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    category_id = fields.Many2one(comodel_name="story.category", string="Category")
    content_ids = fields.One2many(comodel_name="site1.content", inverse_name="story_id")

    prev_id = fields.Many2one(comodel_name="project.site1", string="Previous")
    next_id = fields.Many2one(comodel_name="project.site1", string="Next")

    # Status
    is_valid = fields.Boolean(string="Valid", default=False)
    last_checked_on = fields.Date(string="Last Checked On")
    is_exported = fields.Boolean(string="Exported", default=False)

    def trigger_check_valid(self):
        recs = self.env["project.site1"].search([("is_valid", "=", False)])[:100]

        for rec in recs:
            if rec.title \
                    and rec.preview \
                    and rec.content_ids \
                    and rec.category_id \
                    and rec.site_title \
                    and rec.site_preview \
                    and rec.site_url:

                rec.write({"is_valid": True})

    def trigger_site_data(self):
        recs = self.env["project.site1"].search([("is_valid", "=", False)])[:100]
        for rec in recs:
            rec.write({"site_title": rec.title,
                       "site_preview": rec.preview,
                       "site_url": self.env["other.service"].generate_url(rec.title)})

    def trigger_data_import(self):
        self.next_record_import()
        self.new_record_import()

    def new_record_import(self):
        list_of_random_items = []
        for i in range(5):
            start = i * 200
            end = start + 200
            recs = self.env["story.book"].search([("project_site1", "=", False),
                                                  ("language.name", "=", LANGUAGE),
                                                  ("prev_url", "=", False)])[start:end]

            if len(recs) > NUM_SELECT:
                list_of_random_items = random.sample(recs, NUM_SELECT)

        for rec in list_of_random_items:
            publish = self.env["project.site1"].search_count([("date", "=", datetime.now())])
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

                record_id = self.env["project.site1"].create(data)
                rec.write({"project_site1": record_id.name})

    def next_record_import(self):
        recs = self.env["project.site1"].search([("last_checked_on", "!=", datetime.now()),
                                                 ("is_exported", "=", True),
                                                 ("next_id", "=", False)])[:100]

        for rec in recs:
            story_id = self.env["story.book"].search([("name", "=", rec.ref)])
            if story_id:
                story_obj = self.env["story.book"].search([("prev_url", "=", story_id.crawl_url),
                                                           ("project_site1", "=", False)])
                if story_obj:
                    publish = self.env["project.site1"].search_count([("date", "=", datetime.now())])
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

                        record_id = self.env["project.site1"].create(data)
                        rec.write({"next_id": record_id.id})
                        story_obj.write({"project_site1": record_id.name})

            rec.write({"last_checked_on": datetime.now()})




    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("project.site1")
        return super(ProjectSite1, self).create(vals)


class Site1Content(models.Model):
    _name = "site1.content"
    _description = "Site 1 Content"

    order_seq = fields.Integer(string="Order Sequence")
    content = fields.Text(string="Content")
    story_id = fields.Many2one(comodel_name="project.site1", string="Story")
