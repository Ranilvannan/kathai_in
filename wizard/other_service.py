from odoo import models, fields, api
from odoo.tools import config
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
        file_data.write(tmp, pretty_print=True, xml_declaration=True,   encoding="utf-8")
        tmp.flush()

        return tmp

    def move_tmp_file(self, host, username, key_filename, remote_path, from_file):
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        ssh_client.connect(hostname=host,
                           username=username,
                           key_filename=key_filename)

        sftp_client = ssh_client.open_sftp()
        file_name = os.path.basename(from_file.name)
        to_file = os.path.join(remote_path, file_name)
        sftp_client.put(from_file.name, to_file)
        sftp_client.close()

        return True
