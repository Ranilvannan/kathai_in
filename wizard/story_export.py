from odoo import models, fields
from odoo.tools import config
import tempfile
from datetime import datetime
from paramiko import SSHClient, AutoAddPolicy
import os
import json

HOST = config["story_book_export_host"]
USERNAME = config["story_book_export_username"]
PASSWORD = config["story_book_export_password"]
REMOTE_FILE = config["story_book_export_path"]


class StoryExport(models.TransientModel):
    _name = "story.export"
    _description = "Story Export"

    name = fields.Char(string="Name")

    def trigger_export(self):
        recs = self.env["story.language"].search([])
        for rec in recs:
            export_list = self.env["story.book"].search([("has_published", "=", True),
                                                         ("is_exported", "=", False),
                                                         ("language", "=", rec.id),
                                                         ("date_of_publish", "=", datetime.now())])[:100]
            # export_list = self.env["story.book"].search([("has_published", "=", True)])

            if export_list:
                self.story_export(export_list, rec.name)
                self.category_export(export_list, rec.name)

    def story_export(self, recs, language):
        json_data = self.generate_story_json(recs)
        file_name = "{}_story".format(language)
        tmp_file = self.generate_tmp_file(json_data, file_name)
        # self.move_tmp_file(tmp_file)
        tmp_file.close()

    def category_export(self, recs, language):
        json_data = self.generate_category_json(recs)
        file_name = "{}_category".format(language)
        tmp_file = self.generate_tmp_file(json_data, file_name)
        # self.move_tmp_file(tmp_file)
        tmp_file.close()

    def generate_story_json(self, recs):
        book = []

        for rec in recs:
            story = {
                "story_id": rec.id,
                "published_on": self.date_formatting(rec.date_of_publish),
                "name": rec.name,

                "site_url": rec.site_url,
                "site_title": rec.site_title,
                "site_preview": rec.site_preview,
                "parent_url": rec.parent_id.site_url,
                "tags": [{"name": item.name,
                          "url": item.url} for item in rec.tag_ids],

                "title": rec.title,
                "preview": rec.preview,
                "content_ids": [{"content": item.content,
                                 "order_seq": item.order_seq} for item in rec.content_ids]
            }

            book.append(story)

        return book

    def generate_category_json(self, recs):
        category = []
        cat_id = []
        for rec in recs:
            for item in rec.tag_ids:
                if item.name and item.url and (item.id not in cat_id):
                    category.append({"name": item.name,
                                     "url": item.url})
                    cat_id.append(item.id)

        return category

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

    def generate_tmp_file(self, file_data, file_suffix):
        prefix = datetime.now().strftime('%s')
        suffix = "{}.json".format(file_suffix)
        tmp = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False, mode="w+")
        json.dump(file_data, tmp)
        tmp.flush()

        return tmp

    def date_formatting(self, date):
        formatted = False
        if date:
            formatted = date.strftime("%d-%m-%Y")

        return formatted
