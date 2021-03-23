import os
from odoo import models, fields, api, exceptions
from odoo.tools import config
from datetime import datetime
import requests
import tempfile
import json
from paramiko import SSHClient, AutoAddPolicy

MIN_PUBLISH = 10
DOMAIN = "domain"
LANGUAGE = "English"
HOST = config["story_book_export_host"]
USERNAME = config["story_book_export_username"]
PASSWORD = config["story_book_export_password"]
REMOTE_FILE = config["story_book_export_path"]


class ProjectSite1(models.Model):
    _name = "project.site1"
    _description = "Project Site 1"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    ref = fields.Char(string="Reference")
    date = fields.Date(string="Date", default=datetime.now())

    site_url = fields.Text(string="URL")
    site_title = fields.Text(string="Title")
    site_preview = fields.Text(string="Preview")

    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    category_id = fields.Many2one(comodel_name="story.category", string="Category")
    content_ids = fields.One2many(comodel_name="story.content", inverse_name="story_id")

    prev_id = fields.Many2one(comodel_name="project.site1", string="Previous")
    next_id = fields.Many2one(comodel_name="project.site1", string="Next")

    # Status
    is_valid = fields.Boolean(string="Valid", default=False)
    last_validate_on = fields.Date(string="Last Validate On")
    is_exported = fields.Boolean(string="Exported", default=False)
    url_verified = fields.Boolean(string="URL Verified", default=False)

    def trigger_recs(self):
        publish = self.env["project.site1"].search([("date", "=", datetime.now())]).count()
        if publish <= MIN_PUBLISH:
            recs = self.env["project.site1"].search([("last_validate_on", "=", datetime.now()),
                                                     ("is_exported", "=", True),
                                                     ("next_id", "=", False)])

    def trigger_export(self):
        recs = self.env["project.site1"].search([("is_exported", "=", False),
                                                 ("is_valid", "=", True)])

        if recs:
            self.story_export(recs)
            self.category_export(recs)

        for rec in recs:
            rec.is_exported = True

    def story_export(self, recs):
        json_data = self.generate_story_json(recs)
        file_name = "_{0}_story.json".format(LANGUAGE)
        tmp_file = self.generate_tmp_file(json_data, file_name)
        # self.move_tmp_file(tmp_file)
        tmp_file.close()

    def category_export(self, recs):
        json_data = self.generate_category_json(recs)
        file_name = "_{0}_category.json".format(LANGUAGE)
        tmp_file = self.generate_tmp_file(json_data, file_name)
        # self.move_tmp_file(tmp_file)
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
                "parent_url": rec.parent_id.site_url,
                "category": {"name": rec.category_id.name,
                             "url": rec.category_id.url},

                "title": rec.title,
                "preview": rec.preview,
                "content_ids": [{"content": item.content,
                                 "order_seq": item.order_seq} for item in rec.content_ids],

                "published_on": self.date_formatting(rec.date),
                "language": rec.language.name

            }

            book.append(story)

        return book

    def generate_category_json(self, recs):
        category = []
        cat_id = []
        for rec in recs:
            for item in rec.category_id:
                if item.name and item.url and (item.id not in cat_id):
                    category.append({"name": item.name,
                                     "url": item.url})
                    cat_id.append(item.id)

        return category

    def generate_tmp_file(self, file_data, suffix):
        prefix = datetime.now().strftime('%s')
        tmp = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False, mode="w+")
        json.dump(file_data, tmp)
        tmp.flush()

        return tmp

    def move_tmp_file(self, tmp):
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        ssh_client.connect(hostname=HOST,
                           username=USERNAME,
                           password=PASSWORD)

        sftp_client = ssh_client.open_sftp()
        file_name = os.path.basename(tmp.name)
        sftp_client.put(tmp.name, REMOTE_FILE.format(file_name=file_name))
        sftp_client.close()

    def date_formatting(self, date):
        formatted = False
        if date:
            formatted = date.strftime("%d-%m-%Y")

        return formatted

    def trigger_url_verification(self):
        recs = self.env["project.site1"].search([("url_verified", "=", False),
                                                 ("is_exported", "=", True)])
        for rec in recs:
            url = "https://{0}/story/{1}".format(DOMAIN, rec.site_url)
            site = requests.get(url)
            if site.status_code == 200:
                rec.url_verified = True

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
