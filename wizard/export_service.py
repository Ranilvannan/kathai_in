from odoo import models, fields, api, exceptions
from odoo.tools import config
import os
import json
from datetime import datetime
import tempfile
from paramiko import SSHClient, AutoAddPolicy

PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2")]


class ExportService(models.TransientModel):
    _name = "export.service"
    _description = "Export Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_export(self):
        if self.project == "project_site1":
            self.project_site1_export()

    def project_site1_export(self):
        site_model = "project.site1"
        host = config["story_book_export_host"]
        username = config["story_book_export_username"]
        key_filename = config["story_book_export_public_key_filename"]
        remote_path = config["project_site1_path"]
        lang = config["project_site1_language"]
        story_filename = "_{0}_story.json".format(lang)
        category_filename = "_{0}_category.json".format(lang)

        recs = self.env[site_model].search([("is_exported", "=", False), ("is_valid", "=", True)])

        if recs:
            data = self.generate_json(recs)

            # Story export
            tmp_file = self.generate_tmp_json_file(data["story"])
            self.move_tmp_file(host, username, key_filename, tmp_file, remote_path, story_filename)

            # Category export
            tmp_file = self.generate_tmp_json_file(data["category"])
            self.move_tmp_file(host, username, key_filename, tmp_file, remote_path, category_filename)

        for rec in recs:
            rec.is_exported = True

    def generate_json(self, recs):
        story = []
        cat_id = []
        category = []

        for rec in recs:
            story_data = {
                "story_id": rec.id,
                "name": rec.name,
                "site_url": rec.site_url,
                "site_title": rec.site_title,
                "site_preview": rec.site_preview,
                "title": rec.title,
                "preview": rec.preview,
                "prev": {"name": rec.prev_id.title, "url": rec.prev_id.site_url},
                "next": {"name": rec.next_id.title, "url": rec.next_id.site_url},
                "category": {"name": rec.category_id.name, "url": rec.category_id.url},
                "content_ids": [{"content": item.content, "order_seq": item.order_seq} for item in rec.content_ids],
                "published_on": self.in_format(rec.date)
            }

            category_data = {
                "category_id": rec.category_id.id,
                "name": rec.category_id.name,
                "url": rec.category_id.url,
                "description": rec.category_id.description
                }

            story.append(story_data)
            if rec.category_id.id not in cat_id:
                cat_id.append(rec.category_id.id)
                category.append(category_data)

        return {"story": story, "category": category}

    def generate_tmp_json_file(self, json_data):
        prefix = datetime.now().strftime('%s')
        tmp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=".json", mode="w+")
        json.dump(json_data, tmp_file)
        tmp_file.flush()

        return tmp_file

    def move_tmp_file(self, host, username, key_filename, tmp_file, path, filename):
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(hostname=host, username=username, key_filename=key_filename)
        sftp_client = ssh_client.open_sftp()
        local_path = tmp_file.name
        remote_path = os.path.join(path, filename)
        sftp_client.put(local_path, remote_path)
        sftp_client.close()
        tmp_file.close()

        return True

    def in_format(self, date):
        result = None
        if date and isinstance(date, datetime):
            result = date.strftime("%d-%m-%Y")
        return result
