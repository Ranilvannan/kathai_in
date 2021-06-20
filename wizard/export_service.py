from odoo import models, fields, api, exceptions
from odoo.tools import config
import os
import json
from datetime import datetime
import tempfile
from paramiko import SSHClient, AutoAddPolicy

BLOG_FILENAME = "_blog.json"
CATEGORY_FILENAME = "_category.json"
GALLERY_FILENAME = "_gallery.json"
PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2"),
           ("project_site3", "Project Site 3"),
           ("project_site4", "Project Site 4"),
           ("project_site5", "Project Site 5"),
           ("project_site6", "Project Site 6"),
           ("project_site7", "Project Site 7")]


class ExportService(models.TransientModel):
    _name = "export.service"
    _description = "Export Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def reset_gallery(self):
        recs = self.env["blog.gallery"].search([("is_exported", "=", True)])[:500]

        for rec in recs:
            rec.is_exported = False

    def trigger_export(self):
        site_model = None
        remote_path = config["export_path"]

        if self.project == "project_site1":
            site_model = "project.site1"
        elif self.project == "project_site2":
            site_model = "project.site2"
        elif self.project == "project_site3":
            site_model = "project.site3"
        elif self.project == "project_site4":
            site_model = "project.site4"
        elif self.project == "project_site5":
            site_model = "project.site5"
        elif self.project == "project_site6":
            site_model = "project.site6"
        elif self.project == "project_site7":
            site_model = "project.site7"

        blog_code = self.env[site_model]._blog_code
        blog_filename = "_{0}{1}".format(blog_code, BLOG_FILENAME)
        recs = self.env[site_model].search([("is_exported", "=", False),
                                            ("published_on", "!=", False),
                                            ("is_valid", "=", True)])[:100]

        if recs:
            # Blog export
            blog_list = self.generate_json(recs)
            tmp_file = self.generate_tmp_json_file(blog_list, blog_filename)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def trigger_category_export(self):
        remote_path = config["export_path"]
        recs = self.env["story.category"].search([("id", ">", 0)])
        if recs:
            category_list = self.generate_category_json()
            tmp_file = self.generate_tmp_json_file(category_list, CATEGORY_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def trigger_gallery_export(self):
        remote_path = config["export_path"]
        recs = self.env["blog.gallery"].search([("is_exported", "=", False)])[:500]
        if recs:
            gallery_list = self.generate_gallery_json(recs)
            tmp_file = self.generate_tmp_json_file(gallery_list, GALLERY_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def generate_category_json(self):
        category = []
        recs = self.env["story.category"].search([("id", ">", 0)])
        for rec in recs:
            data = {
                "category_id": rec.id,
                "name": rec.name,
                "url": rec.url,
                "language": rec.language
            }
            category.append(data)

        return category

    def generate_json(self, recs):
        story = []

        for rec in recs:
            data = {
                "blog_id": rec.id,
                "blog_code": rec._blog_code,
                "language": rec._language,
                "name": rec.name,
                "url": rec.url,
                "title": rec.title,
                "preview": rec.preview,
                "image_filename": rec.gallery_id.filename,
                "image_filepath": rec.gallery_id.filepath,
                "image_description": rec.gallery_id.description,
                "galleries": [{"image_filename": gallery.filename,
                               "image_filepath": gallery.filepath,
                               "image_description": gallery.description} for gallery in rec.gallery_ids],
                "previous_title": rec.prev_id.title,
                "previous_url": rec.prev_id.url,
                "next_title": rec.next_id.title,
                "next_url": rec.next_id.url,
                "category_name": rec.category_id.name,
                "category_url": rec.category_id.url,
                "content_ids": rec.content.split("|#|"),
                "published_on": rec.published_on.strftime("%d-%m-%Y") if rec.published_on else None,
                "date": rec.published_on.isoformat() if rec.published_on else None
            }

            story.append(data)

        return story

    def generate_gallery_json(self, recs):
        galleries = []

        for rec in recs:
            image = {
                "gallery_id": rec.id,
                "filename": rec.filename,
                "filepath": rec.filepath,
                "description": rec.description
            }
            galleries.append(image)

        return galleries

    def generate_tmp_json_file(self, json_data, suffix):
        prefix = datetime.now().strftime('%s')
        tmp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False, mode="w+")
        json.dump(json_data, tmp_file)
        tmp_file.flush()

        return tmp_file

    def move_tmp_file(self, tmp_file, path):
        host = config["export_host"]
        username = config["export_username"]
        key_filename = config["export_public_key_filename"]

        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(hostname=host, username=username, key_filename=key_filename)
        sftp_client = ssh_client.open_sftp()
        filename = os.path.basename(tmp_file.name)
        local_path = tmp_file.name
        remote_path = os.path.join(path, filename)
        sftp_client.put(local_path, remote_path)
        sftp_client.close()
        tmp_file.close()

        return True
