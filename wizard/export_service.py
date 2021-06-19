from odoo import models, fields, api, exceptions
from odoo.tools import config
import os
import json
from datetime import datetime
import tempfile
from paramiko import SSHClient, AutoAddPolicy

BLOG_FILENAME = "_blog.json"
CATEGORY_FILENAME = "_category.json"
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

    def trigger_export(self):
        if self.project == "project_site1":
            self.project_site1_export()
        elif self.project == "project_site2":
            self.project_site2_export()
        elif self.project == "project_site3":
            self.project_site3_export()
        elif self.project == "project_site4":
            self.project_site4_export()
        elif self.project == "project_site5":
            self.project_site5_export()
        elif self.project == "project_site6":
            self.project_site6_export()
        elif self.project == "project_site7":
            self.project_site7_export()

    def project_site1_export(self):
        site_model = "project.site1"
        remote_path = config["project_site1_path"]
        lang = "English"
        
        recs = self.env[site_model].search([("is_exported", "=", False),
                                            ("published_on", "!=", False),
                                            ("is_valid", "=", True)])[:100]

        if recs:
            # Blog export
            blog_list = self.generate_json(recs, lang)
            tmp_file = self.generate_tmp_json_file(blog_list, BLOG_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        # Category export
        category_list = self.generate_category(site_model, lang)
        if category_list:
            tmp_file = self.generate_tmp_json_file(category_list, CATEGORY_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def project_site2_export(self):
        site_model = "project.site2"
        remote_path = config["project_site2_path"]
        lang = "Tamil"
        
        recs = self.env[site_model].search([("is_exported", "=", False),
                                            ("published_on", "!=", False),
                                            ("is_valid", "=", True)])[:100]

        if recs:
            # Blog export
            blog_list = self.generate_json(recs, lang)
            tmp_file = self.generate_tmp_json_file(blog_list, BLOG_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        # Category export
        category_list = self.generate_category(site_model, lang)
        if category_list:
            tmp_file = self.generate_tmp_json_file(category_list, CATEGORY_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def project_site3_export(self):
        site_model = "project.site3"
        remote_path = config["project_site3_path"]
        lang = "Hindi"
        
        recs = self.env[site_model].search([("is_exported", "=", False),
                                            ("published_on", "!=", False),
                                            ("is_valid", "=", True)])[:100]

        if recs:
            # Blog export
            blog_list = self.generate_json(recs, lang)
            tmp_file = self.generate_tmp_json_file(blog_list, BLOG_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        # Category export
        category_list = self.generate_category(site_model, lang)
        if category_list:
            tmp_file = self.generate_tmp_json_file(category_list, CATEGORY_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def project_site4_export(self):
        site_model = "project.site4"
        remote_path = config["project_site4_path"]
        lang = "Malayalam"

        recs = self.env[site_model].search([("is_exported", "=", False),
                                            ("published_on", "!=", False),
                                            ("is_valid", "=", True)])[:100]

        if recs:
            # Blog export
            blog_list = self.generate_json(recs, lang)
            tmp_file = self.generate_tmp_json_file(blog_list, BLOG_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        # Category export
        category_list = self.generate_category(site_model, lang)
        if category_list:
            tmp_file = self.generate_tmp_json_file(category_list, CATEGORY_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def project_site5_export(self):
        site_model = "project.site5"
        remote_path = config["project_site5_path"]
        lang = "Telugu"

        recs = self.env[site_model].search([("is_exported", "=", False),
                                            ("published_on", "!=", False),
                                            ("is_valid", "=", True)])[:100]

        if recs:
            # Blog export
            blog_list = self.generate_json(recs, lang)
            tmp_file = self.generate_tmp_json_file(blog_list, BLOG_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        # Category export
        category_list = self.generate_category(site_model, lang)
        if category_list:
            tmp_file = self.generate_tmp_json_file(category_list, CATEGORY_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def project_site6_export(self):
        site_model = "project.site6"
        remote_path = config["project_site6_path"]
        lang = "Telugu"

        recs = self.env[site_model].search([("is_exported", "=", False),
                                            ("published_on", "!=", False),
                                            ("is_valid", "=", True)])[:100]

        if recs:
            # Blog export
            blog_list = self.generate_json(recs, lang)
            tmp_file = self.generate_tmp_json_file(blog_list, BLOG_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        # Category export
        category_list = self.generate_category(site_model, lang)
        if category_list:
            tmp_file = self.generate_tmp_json_file(category_list, CATEGORY_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def project_site7_export(self):
        site_model = "project.site7"
        remote_path = config["project_site7_path"]
        lang = "Bengali"

        recs = self.env[site_model].search([("is_exported", "=", False),
                                            ("published_on", "!=", False),
                                            ("is_valid", "=", True)])[:100]

        if recs:
            # Blog export
            blog_list = self.generate_json(recs, lang)
            tmp_file = self.generate_tmp_json_file(blog_list, BLOG_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        # Category export
        category_list = self.generate_category(site_model, lang)
        if category_list:
            tmp_file = self.generate_tmp_json_file(category_list, CATEGORY_FILENAME)
            self.move_tmp_file(tmp_file, remote_path)

        for rec in recs:
            rec.is_exported = True

    def generate_category(self, site_model, lang):
        category = []
        recs = self.env["story.category"].search([("language", "=", lang)])
        for rec in recs:
            story = self.env[site_model].search([("category_id", "=", rec.id)])
            if story:
                data = {
                    "category_id": rec.id,
                    "name": rec.name,
                    "url": rec.url
                }
                category.append(data)

        return category

    def generate_json(self, recs, lang):
        story = []

        for rec in recs:
            data = {
                "blog_id": rec.id,
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
                "date": rec.published_on.isoformat() if rec.published_on else None,
                "language": lang
            }

            story.append(data)

        return story

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
