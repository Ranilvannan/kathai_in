from odoo import models, fields
import string
import random
from itertools import groupby
from operator import itemgetter
import unicodedata
from .translator import translate
from .preview_key import key_list

PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2"),
           ("project_site3", "Project Site 3"),
           ("project_site4", "Project Site 4"),
           ("project_site5", "Project Site 5"),
           ("project_site6", "Project Site 6"),
           ("project_site7", "Project Site 7")]


class SiteUpdateService(models.TransientModel):
    _name = "site.update.service"
    _description = "Site Update Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_site_update(self):
        if self.project == "project_site1":
            self.project_site_update(site_model="project.site1")
        elif self.project == "project_site2":
            self.project_site_update(site_model="project.site2")
        elif self.project == "project_site3":
            self.project_site_update(site_model="project.site3")
        elif self.project == "project_site4":
            self.project_site_update(site_model="project.site4")
        elif self.project == "project_site5":
            self.project_site_update(site_model="project.site5")
        elif self.project == "project_site6":
            self.project_site_update(site_model="project.site6")
        elif self.project == "project_site7":
            self.project_site_update(site_model="project.site7")

    def project_site_update(self, site_model):
        recs = self.env[site_model].search([("is_valid", "=", False)])[:100]
        for rec in recs:
            preview = self.generate_preview(rec.content)
            title = self.get_translated_text(rec.title).title()

            rec.write({"preview": preview,
                       "url": self.generate_url(title)})

    def generate_preview(self, content):
        preview_data = False
        recs = content.split("|#|")[:10]

        if not preview_data:
            for rec in recs:
                for data in key_list:
                    if rec.find(data) > 0 and (not preview_data):
                        preview_data = rec

        if not preview_data:
            for rec in recs:
                space_list = rec.split(" ")
                if len(space_list) >= 24 and (not preview_data):
                    preview_data = rec

        if not preview_data:
            content_len = len(recs)
            if content_len >= 4 and (not preview_data):
                preview_data = recs[4]

        if not preview_data:
            content_len = len(recs)
            if content_len >= 1 and (not preview_data):
                preview_data = recs[1]

        return preview_data

    def get_translated_text(self, text):
        result = translate(text)
        return self.strip_accents(result)

    def strip_accents(self, text):
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text)

    def generate_url(self, text):
        new_text = "".join([c if c.isalnum() else "-" for c in text.lower()])
        new_text = "".join(map(next, map(itemgetter(1), groupby(new_text))))
        res = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
        site_path = "{0}-{1}".format(new_text, res)
        return site_path
