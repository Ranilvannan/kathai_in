from odoo import models, fields
import string
import random
from itertools import groupby
from operator import itemgetter
import unicodedata
from .translator import translate

PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2")]


class SiteUpdateService(models.TransientModel):
    _name = "site.update.service"
    _description = "Site Update Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_site_update(self):
        if self.project == "project_site1":
            self.project_site1_update(site_model="project.site1")

    def project_site1_update(self, site_model):
        recs = self.env[site_model].search([("is_valid", "=", False)])[:100]
        for rec in recs:
            site_title = self.get_translated_text(rec.title)
            site_preview = self.get_translated_text(rec.preview)

            rec.write({"site_title": site_title,
                       "site_preview": site_preview,
                       "site_url": self.generate_url(site_title)})

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
