from odoo import models, fields, api
import os
from datetime import datetime
import string
import random
from itertools import groupby
from operator import itemgetter
import tempfile
import json
from paramiko import SSHClient, AutoAddPolicy


class OtherService(models.TransientModel):
    _name = "other.service"
    _description = "Other Service"

    def generate_url(self, text):
        new_text = "".join([c if c.isalnum() else "-" for c in text.lower()])
        new_text = "".join(map(next, map(itemgetter(1), groupby(new_text))))
        res = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
        site_path = "{0}-{1}".format(new_text, res)
        return site_path

    def generate_json_tmp_file(self, file_data, suffix):
        prefix = datetime.now().strftime('%s')
        tmp = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False, mode="w+")
        json.dump(file_data, tmp)
        tmp.flush()

        return tmp

    def generate_tmp_xml_file(self, file_data, suffix):
        prefix = datetime.now().strftime('%s')
        tmp = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False, mode="wb+")
        tmp.write(file_data)
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
