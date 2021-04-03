from odoo import models, fields, api, exceptions
from odoo.tools import config
import os
from datetime import datetime
import requests
import random

MIN_PUBLISH = 20
NUM_SELECT = 2
PER_PAGE = 9
LANGUAGE = "Tamil"

DOMAIN = config["project_site2_domain"]
HOST = config["story_book_export_host"]
USERNAME = config["story_book_export_username"]
KEY_FILENAME = config["story_book_export_public_key_filename"]
REMOTE_FILE = config["project_site2_path"]


class ProjectSite2(models.Model):
    _name = "project.site2"
    _description = "Project Site 2 tamilsexstory.osholikes"
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
    content_ids = fields.One2many(comodel_name="site2.content", inverse_name="story_id")

    prev_id = fields.Many2one(comodel_name="project.site2", string="Previous")
    next_id = fields.Many2one(comodel_name="project.site2", string="Next")

    # Status
    is_valid = fields.Boolean(string="Valid", default=False)
    last_checked_on = fields.Date(string="Last Checked On")
    is_exported = fields.Boolean(string="Exported", default=False)
    url_verified = fields.Boolean(string="URL Verified", default=False)

    def trigger_check_valid(self):
        recs = self.env["project.site2"].search([("is_valid", "=", False)])[:100]

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
        recs = self.env["project.site2"].search([("is_valid", "=", False)])[:100]
        for rec in recs:
            site_title = self.env["other.service"].get_translated_text(rec.title)
            site_preview = self.env["other.service"].get_translated_text(rec.preview)
            rec.write({"site_title": site_title,
                       "site_preview": site_preview,
                       "site_url": self.env["other.service"].generate_url(site_title)})

    def trigger_data_import(self):
        self.next_record_import()
        self.new_record_import()

    def new_record_import(self):
        recs = self.env["story.book"].search([("project_site2", "=", False),
                                              ("language.name", "=", LANGUAGE),
                                              ("prev_url", "=", False)])[:300]
        list_of_random_items = []
        if len(recs) > NUM_SELECT:
            list_of_random_items = random.sample(recs, NUM_SELECT)

        for rec in list_of_random_items:
            publish = self.env["project.site2"].search_count([("date", "=", datetime.now())])
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

                record_id = self.env["project.site2"].create(data)
                rec.write({"project_site2": record_id.name})

    def next_record_import(self):
        recs = self.env["project.site2"].search([("last_checked_on", "!=", datetime.now()),
                                                 ("is_exported", "=", True),
                                                 ("next_id", "=", False)])[:100]

        for rec in recs:
            story_id = self.env["story.book"].search([("name", "=", rec.ref)])
            if story_id:
                story_obj = self.env["story.book"].search([("prev_url", "=", story_id.crawl_url),
                                                           ("project_site2", "=", False)])
                if story_obj:
                    publish = self.env["project.site2"].search_count([("date", "=", datetime.now())])
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

                        record_id = self.env["project.site2"].create(data)
                        rec.write({"next_id": record_id.id})
                        story_obj.write({"project_site2": record_id.name})

            rec.write({"last_checked_on": datetime.now()})

    def trigger_export(self):
        recs = self.env["project.site2"].search([("is_exported", "=", False),
                                                 ("is_valid", "=", True)])

        if recs:
            # Story export
            story_json = self.generate_story_json(recs)
            story_filename = "_{0}_story.json".format(LANGUAGE)
            self.generate_and_export(story_json, story_filename)

            # Category export
            category_json = self.generate_category_json(recs)
            category_filename = "_{0}_category.json".format(LANGUAGE)
            self.generate_and_export(category_json, category_filename)

        for rec in recs:
            rec.is_exported = True

    def generate_and_export(self, json_data, file_name):
        tmp_file = self.env["other.service"].generate_json_tmp_file(json_data, file_name)
        to_file = os.path.basename(tmp_file.name)
        remote_path = os.path.join(REMOTE_FILE, to_file)
        self.env["other.service"].move_tmp_file(HOST, USERNAME, KEY_FILENAME, tmp_file.name, remote_path)
        tmp_file.close()

    def generate_story_json(self, recs):
        book = []

        for rec in recs:
            story = {
                "story_id": rec.id,
                "name": rec.name,

                "site_url": rec.site_url,
                "site_title": rec.site_title,
                "site_preview": rec.site_preview,
                "prev": {"name": rec.prev_id.title,
                         "url": rec.prev_id.site_url},
                "next": {"name": rec.next_id.title,
                         "url": rec.next_id.site_url},
                "category": {"name": rec.category_id.name,
                             "url": rec.category_id.url},

                "title": rec.title,
                "preview": rec.preview,
                "content_ids": [{"content": item.content,
                                 "order_seq": item.order_seq} for item in rec.content_ids],

                "published_on": rec.get_published_on_in_format(),
                "language": LANGUAGE

            }

            book.append(story)

        return book

    def generate_category_json(self, recs):
        book = []
        cat_id = []
        for rec in recs:
            for item in rec.category_id:
                if item.name and item.url and (item.id not in cat_id):
                    category = {
                        "category_id": item.id,
                        "name": item.name,
                        "url": item.url,
                        "description": item.description
                    }
                    book.append(category)
                    cat_id.append(item.id)

        return book

    def trigger_url_verification(self):
        recs = self.env["project.site2"].search([("url_verified", "=", False),
                                                 ("is_exported", "=", True)])
        for rec in recs:
            url = "https://{0}story/{1}".format(DOMAIN, rec.site_url)
            site = requests.get(url)
            if site.status_code == 200:
                rec.url_verified = True

    def get_published_on_us_format(self):
        result = None
        if self.date:
            result = self.date.strftime("%Y-%m-%d")
        return result

    def get_published_on_in_format(self):
        result = None
        if self.date:
            result = self.date.strftime("%d-%m-%Y")
        return result

    def home_page_urls(self):
        result = []
        count = self.env["project.site2"].search_count([("is_exported", ">=", True)])

        if count:
            total_page = int(count / PER_PAGE) + 1
            for page in range(1, total_page):
                loc = "{0}turn/{1}/".format(DOMAIN, page)
                lastmod = datetime.now().strftime("%Y-%m-%d")
                result.append({"loc": loc, "lastmod": lastmod})

        return result

    def category_page_urls(self):
        result = []
        category_ids = self.env["story.category"].search([])

        for category_id in category_ids:
            count = self.env["project.site2"].search_count([("is_exported", ">=", True),
                                                            ("category_id", "=", category_id.id)])

            if count:
                total_page = int(count/PER_PAGE) + 1
                for page in range(1, total_page):
                    loc = "{0}category/{1}/turn/{2}/".format(DOMAIN, category_id.url, page)
                    lastmod = datetime.now().strftime("%Y-%m-%d")
                    result.append({"loc": loc, "lastmod": lastmod})

        return result

    def story_page_urls(self, from_date, till_date):
        result = []
        recs = self.env["project.site2"].search([("date", ">=", from_date),
                                                 ("date", "<=", till_date),
                                                 ("is_exported", "=", True)])

        for rec in recs:
            loc = "{0}story/{1}/".format(DOMAIN, rec.site_url)
            result.append({"loc": loc,
                           "lastmod": rec.get_published_on_us_format()})

        return result

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("project.site2")
        return super(ProjectSite2, self).create(vals)


class Site2Content(models.Model):
    _name = "site2.content"
    _description = "Site 2 Content"

    order_seq = fields.Integer(string="Order Sequence")
    content = fields.Text(string="Content")
    story_id = fields.Many2one(comodel_name="project.site2", string="Story")