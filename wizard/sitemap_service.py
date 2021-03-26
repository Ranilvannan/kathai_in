from odoo import models, fields, api
from odoo.tools import config
import os
from datetime import datetime
import calendar
from lxml import etree
from xml.etree.ElementTree import Element, SubElement, tostring
import tempfile
from paramiko import SSHClient, AutoAddPolicy
from xml.dom import minidom

HOST = config["story_book_export_host"]
USERNAME = config["story_book_export_username"]
KEY_FILENAME = config["story_book_export_public_key_filename"]
REMOTE_FILE = "/home/vetrivel/english/sitemap/{filename}"

MONTH = [("1", "January")]
YEAR = [("2021", "2021"), ("2022", "2022")]
SITE = [("project.site1", "Project Site 1")]


class SitemapService(models.TransientModel):
    _name = "sitemap.service"
    _description = "Sitemap Service"

    month = fields.Selection(selection=MONTH, string="Months")
    year = fields.Selection(selection=YEAR, string="Year")
    site = fields.Selection(selection=SITE, string="Site", required=True)

    def trigger_this_month_sitemap(self):
        year_now = datetime.now().strftime("%Y")
        month_now = datetime.now().strftime("%m")

        day = calendar.monthrange(int(year_now), int(month_now))
        from_date = "{0}-{1}-{2}".format(year_now, month_now, "01")
        till_date = "{0}-{1}-{2}".format(year_now, month_now, day[1])
        site_model = self.site
        month_name = datetime.now().strftime("%B").lower()
        filename = "{0}_sitemap.xml".format(month_name)

        recs = self.env[site_model].story_page_urls(from_date, till_date)
        data = self.generate_sitemap_xml_data(recs)
        self.generate_tmp_file(data, filename)

    def generate_sitemap_xml_data(self, recs):
        urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        for rec in recs:
            url = SubElement(urlset, "url")
            SubElement(url, "loc").text = rec["loc"]
            SubElement(url, "lastmod").text = rec["lastmod"]
            SubElement(url, "changefreq").text = "monthly"
            SubElement(url, "priority").text = "0.5"

        xml_string = tostring(urlset)
        xml_page = minidom.parseString(xml_string)
        data = xml_page.toprettyxml()

        return data

    def move_tmp_file(self, tmp, filename):
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        ssh_client.connect(hostname=HOST,
                           username=USERNAME,
                           key_filename=KEY_FILENAME)

        sftp_client = ssh_client.open_sftp()
        sftp_client.put(tmp.name, REMOTE_FILE.format(filename=filename))
        sftp_client.close()

    def generate_tmp_file(self, file_data, filename):
        prefix = datetime.now().strftime('%s')
        with tempfile.NamedTemporaryFile(prefix=prefix, suffix=".xml") as tmp:
            data = str.encode(file_data)
            tmp.write(data)
            tmp.flush()
            self.move_tmp_file(tmp, filename)

    def trigger_monthly_sitemap(self):
        pass

    def trigger_page_wise_sitemap(self):
        pass
