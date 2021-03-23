from odoo import models, fields, api
from datetime import datetime
import string
import random
from itertools import groupby
from operator import itemgetter


class OtherService(models.Model):
    _name = "other.service"
    _description = "Other Service"

    def generate_url(self, text):
        new_text = "".join([c if c.isalnum() else "-" for c in text.lower()])
        new_text = "".join(map(next, map(itemgetter(1), groupby(new_text))))
        res = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
        site_path = "{0}-{1}".format(new_text, res)
        return site_path
