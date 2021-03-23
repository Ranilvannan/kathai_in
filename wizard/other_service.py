from odoo import models, fields, api
from datetime import datetime
import string
import random


class OtherService(models.Model):
    _name = "other.service"
    _description = "Other Service"

    def generate_url(self, text):
        new_text = text.lower()
        new_text = new_text.replace(" ", "-")
        new_text = new_text.replace("'", "")
        new_text = new_text.replace(",", "")

        res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
        site_path = "{0}-{1}".format(new_text, res)
        return site_path
