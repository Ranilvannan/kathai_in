from odoo import models, fields
from odoo.tools import config
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import tempfile
from datetime import datetime
from paramiko import SSHClient, AutoAddPolicy
import os

HOST = config["kathai_in_export_host"]
USERNAME = config["kathai_in_export_username"]
PASSWORD = config["kathai_in_export_password"]
REMOTE_FILE = config["kathai_in_export_path"]

CRAWL_URL_1 = config["kathai_in_crawl_1"]


class KathaiInExport(models.TransientModel):
    _name = "kathai.in.export"
    _description = "Story Export"

    name = fields.Char(string="Name")

    def trigger_export(self):
        # Todo: Add status in production deployment
        # recs = self.env["kathai.in.story"].search([("status", "=", "content_crawl"),
        #                                       ("is_exported", "=", False)])
        # recs = self.env["kathai.in.story"].search([("is_exported", "=", False)])

        recs = self.env["kathai.in.story"].search([])
        print(recs, "---")

        xml_data = self.construct_xml(recs)
        print(xml_data)
        # self.generate_tmp_file(xml_data)

    def construct_xml(self, recs):
        book = Element('book')
        for rec in recs:

            if rec.content_ids:
                story = SubElement(book, 'story')

                sequence = SubElement(story, 'sequence')
                sequence.text = rec.sequence

                title = SubElement(story, 'title')
                title.text = rec.title

                preview = SubElement(story, 'preview')
                preview.text = rec.preview

                for line in rec.content_ids:
                    content = SubElement(story, 'content', {"order_seq": str(line.order_seq)})
                    content.text = line.paragraph

        xml_string = tostring(book)
        xml_page = minidom.parseString(xml_string)
        data = xml_page.toprettyxml()

        return data

    def move_tmp_file(self, tmp):
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        ssh_client.connect(hostname=HOST,
                           username=USERNAME,
                           password=PASSWORD)

        sftp_client = ssh_client.open_sftp()
        file_name = os.path.basename(tmp.name)
        sftp_client.put(tmp.name, REMOTE_FILE.format(file_name=file_name))
        sftp_client.close()

    def generate_tmp_file(self, file_data):
        prefix = datetime.now().strftime('%s')
        with tempfile.NamedTemporaryFile(prefix=prefix, suffix=".xml") as tmp:
            data = str.encode(file_data)
            tmp.write(data)
            tmp.flush()
            self.move_tmp_file(tmp)

