from odoo import models, fields, api, exceptions
import os
from datetime import datetime
import calendar
from lxml import etree
import tempfile
from paramiko import SSHClient, AutoAddPolicy


MONTH = [("01", "January"),
         ("02", "February"),
         ("03", "March"),
         ("04", "April"),
         ("05", "May"),
         ("06", "June"),
         ("07", "July"),
         ("08", "August"),
         ("09", "September"),
         ("10", "October"),
         ("11", "November"),
         ("12", "December")]
YEAR = [("2021", "2021"), ("2022", "2022")]
PROJECT = [("project_site1", "Project Site 1"),
           ("project_site2", "Project Site 2")]
INDEX_FILENAME = "sitemap.xml"
ARTICLE_FILENAME = "{0}_{1}_sitemap.xml"


class SitemapService(models.TransientModel):
    _name = "sitemap.service"
    _description = "Sitemap Service"

    month = fields.Selection(selection=MONTH, string="Months", required=1)
    year = fields.Selection(selection=YEAR, string="Year", required=1)
    project = fields.Selection(selection=PROJECT, string="Project", required=1)

    def trigger_sitemap(self):
        if self.project == "project_site1":
            self.project_site1_sitemap()

    def project_site1_sitemap(self):
        host = ""
        username = ""
        key_file = ""
        path = ""
        domain = ""


    def page_sitemap(self):
        pass

    def article_sitemap(self, site_model, remote_path, domain):
        day = calendar.monthrange(int(self.year), int(self.month))
        from_date = "{0}-{1}-{2}".format(self.year, self.month, "01")
        till_date = "{0}-{1}-{2}".format(self.year, self.month, day[1])
        date_obj = datetime.strptime(from_date, "%d-%m-%Y")
        month_name = date_obj.strftime("%B").lower()

        filename = ARTICLE_FILENAME.format(month_name, self.year)
        filepath = os.path.join(remote_path, "sitemap", filename)

        result = []
        recs = self.env[site_model].search([("date", ">=", from_date),
                                            ("date", "<=", till_date),
                                            ("is_exported", "=", True)])

        for rec in recs:
            url = [domain, "category", rec.category_id.url, rec.site_url]
            result.append({"loc": "/".join(url),
                           "lastmod": rec.get_published_on_us_format()})

        self.generate_sitemap_xml_data(result, "monthly")

    def generate_sitemap_xml_data(self, recs, change_freq):
        urlset = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        for rec in recs:
            url = etree.SubElement(urlset, "url")
            etree.SubElement(url, "loc").text = rec["loc"]
            etree.SubElement(url, "lastmod").text = rec["lastmod"]
            etree.SubElement(url, "changefreq").text = change_freq
            etree.SubElement(url, "priority").text = "0.5"

        data = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding="utf-8")

        return data

    def generate_tmp_xml_file(self, xml_data, suffix):
        prefix = datetime.now().strftime('%s')
        tmp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False, mode="w+")
        xml_data.write(tmp_file, pretty_print=True, xml_declaration=True, encoding="utf-8")
        tmp_file.flush()

        return tmp_file
