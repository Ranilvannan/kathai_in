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
from paramiko import SSHClient, AutoAddPolicy


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

    def generate_json_tmp_file(self, file_data, suffix):
        prefix = datetime.now().strftime('%s')
        tmp = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, mode="w+")
        json.dump(file_data, tmp)
        tmp.flush()

        return tmp

    def move_tmp_file(self, host, username, key_filename, local_path, remote_path):
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        ssh_client.connect(hostname=host,
                           username=username,
                           key_filename=key_filename)

        sftp_client = ssh_client.open_sftp()
        sftp_client.put(local_path, remote_path)
        sftp_client.close()

        return True

    def export_reset(self, site_model):
        obj = self.env[site_model]
        un_exported = obj.search_count([("is_exported", "=", False)])
        if un_exported:
            raise exceptions.ValidationError("Error! Reset needs all records to be exported")

        recs = obj.search([])

        for rec in recs:
            rec.is_exported = False
