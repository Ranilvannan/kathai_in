from odoo import models, fields, api, exceptions
import string
import random
from itertools import groupby
from operator import itemgetter
import unicodedata
from .translator import translate


class TranslationService(models.TransientModel):
    _name = "translation.service"
    _description = "Translation Service"

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
