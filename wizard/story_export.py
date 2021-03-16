from odoo import models, fields
from odoo.tools import config
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
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
        recs = self.env["story.book"].search([("has_published", "=", True),
                                              ("is_exported", "=", False),
                                              ("date_of_publish", "=", datetime.now())])[:100]
        print(recs, "---")
        if recs:
            json_data = self.generate_json(recs)
            tmp_file = self.generate_tmp_file(json_data)
            # self.move_tmp_file(tmp_file)
            tmp_file.close()

    def generate_json(self, recs):
        book = []

        for rec in recs:
            story = {
                "story_id": rec.id,
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

    def generate_tmp_file(self, file_data):
        prefix = datetime.now().strftime('%s')
        tmp = tempfile.NamedTemporaryFile(prefix=prefix, suffix=".json", delete=False, mode="w+")
        json.dump(file_data, tmp)
        tmp.flush()

        return tmp

    def trigger_set_parent_id(self):
        recs = self.env["story.book"].search([("crawl_status", "=", "content_crawl"),
                                              ("is_translated", "=", True),
                                              ("parent_url", "!=", False),
                                              ("parent_id", "=", False),
                                              ("has_published", "=", False)])

        for rec in recs:
            obj = self.env["story.book"].search([("crawl_url", "=", rec.parent_url)])
            if len(obj) == 1:
                rec.parent_id = obj.id
            else:
                rec.active = False

    def trigger_publish(self):
        recs = self.env["story.book"].search([("crawl_status", "=", "content_crawl"),
                                              ("has_published", "=", False)])[:100]

        for rec in recs:
            rec.trigger_publish()
