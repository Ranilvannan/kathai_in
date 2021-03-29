from odoo import models, fields, api
from odoo.tools import config
import os
from datetime import datetime
import calendar
from lxml import etree


HOST = config["story_book_export_host"]
USERNAME = config["story_book_export_username"]
KEY_FILENAME = config["story_book_export_public_key_filename"]


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
SITE = [("project_site1", "Project Site 1")]


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

        if self.site == "project_site1":
            remote_path = config["project_site1_path"]
            self.article_sitemap("project.site1", remote_path, from_date, till_date, "monthly")
            self.index_sitemap("project.site1", remote_path, "daily")

    def index_sitemap(self, site_model, remote_path, frequency):
        filename = "sitemap.xml"
        filepath = os.path.join(remote_path, "sitemap", filename)

        recs = self.env[site_model].home_page_urls()
        category_page_list = self.env[site_model].category_page_urls()
        recs.extend(category_page_list)
        file_data = self.generate_sitemap_xml_data(recs, frequency)
        tmp_file = self.env["other.service"].generate_tmp_xml_file(file_data, filename)

        self.env["other.service"].move_tmp_file(HOST, USERNAME, KEY_FILENAME, tmp_file.name, filepath)
        tmp_file.close()

    def article_sitemap(self, site_model, remote_path, from_date, till_date, frequency):
        month_name = datetime.now().strftime("%B").lower()
        year = datetime.now().strftime("%Y").lower()
        filename = "{0}_{1}_sitemap.xml".format(month_name, year)
        filepath = os.path.join(remote_path, "sitemap", filename)

        recs = self.env[site_model].story_page_urls(from_date, till_date)
        file_data = self.generate_sitemap_xml_data(recs, frequency)
        tmp_file = self.env["other.service"].generate_tmp_xml_file(file_data, filename)

        self.env["other.service"].move_tmp_file(HOST, USERNAME, KEY_FILENAME, tmp_file.name, filepath)
        tmp_file.close()

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
