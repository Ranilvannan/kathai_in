from odoo import models, fields, api, exceptions
import os
from datetime import datetime
import string
import random
from itertools import groupby
from operator import itemgetter
import tempfile
import json
import unicodedata
from .translator import translate



class OtherService(models.TransientModel):
    _name = "other.service"
    _description = "Other Service"

    def in_format(self, date):
        result = None
        if date and isinstance(date, datetime):
            result = self.date.strftime("%d-%m-%Y")
        return result

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



    def export_reset(self, site_model):
        obj = self.env[site_model]
        un_exported = obj.search_count([("is_exported", "=", False)])
        if un_exported:
            raise exceptions.ValidationError("Error! Reset needs all records to be exported")

        recs = obj.search([])

        for rec in recs:
            rec.is_exported = False
