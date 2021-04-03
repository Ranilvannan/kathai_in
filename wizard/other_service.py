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





    def export_reset(self, site_model):
        obj = self.env[site_model]
        un_exported = obj.search_count([("is_exported", "=", False)])
        if un_exported:
            raise exceptions.ValidationError("Error! Reset needs all records to be exported")

        recs = obj.search([])

        for rec in recs:
            rec.is_exported = False
