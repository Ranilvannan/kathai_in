from odoo import models, fields, api, exceptions
from odoo.tools import config
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
        elif self.project == "project_site2":
            self.project_site2_sitemap()

    def project_site1_sitemap(self):
        site_model = "project.site1"
        host = config["story_book_export_host"]
        username = config["story_book_export_username"]
        key_file = config["story_book_export_public_key_filename"]
        remote_path = config["project_site1_path"]
        domain = config["project_site1_domain"]
        per_page = 9

        self.article_sitemap(site_model, domain, host, username, key_file, remote_path)
        self.page_sitemap(site_model, domain, host, username, key_file, remote_path, per_page)

    def project_site2_sitemap(self):
        site_model = "project.site2"
        host = config["story_book_export_host"]
        username = config["story_book_export_username"]
        key_file = config["story_book_export_public_key_filename"]
        remote_path = config["project_site2_path"]
        domain = config["project_site2_domain"]
        per_page = 9

        self.article_sitemap(site_model, domain, host, username, key_file, remote_path)
        self.page_sitemap(site_model, domain, host, username, key_file, remote_path, per_page)

    def home_page_urls(self, site_model, domain, per_page):
        result = []
        count = self.env[site_model].search_count([("is_exported", ">=", True),
                                                   ("published_on", "<=", datetime.now())])

        if count:
            total_page = int(count / per_page) + 1
            for page in range(1, total_page):
                if page == 1:
                    loc = domain
                else:
                    loc = "{0}/page/{1}/".format(domain, page)
                lastmod = datetime.now().strftime("%Y-%m-%d")
                result.append({"loc": loc, "lastmod": lastmod})

        return result

    def category_page_urls(self, site_model, domain, per_page):
        result = []
        category_ids = self.env["story.category"].search([])

        for category_id in category_ids:
            count = self.env[site_model].search_count([("is_exported", ">=", True),
                                                       ("category_id", "=", category_id.id),
                                                       ("published_on", "<=", datetime.now())])

            if count:
                total_page = int(count/per_page) + 1
                for page in range(1, total_page):
                    if page == 1:
                        loc = "{0}/category/{1}/".format(domain, category_id.url)
                    else:
                        loc = "{0}/category/{1}/page/{2}/".format(domain, category_id.url, page)
                    lastmod = datetime.now().strftime("%Y-%m-%d")
                    result.append({"loc": loc, "lastmod": lastmod})

        return result

    def page_sitemap(self, site_model, domain, host, username, key_file, remote_path, per_page):
        filename = INDEX_FILENAME

        recs = self.home_page_urls(site_model, domain, per_page)
        category_page_list = self.category_page_urls(site_model, domain, per_page)
        recs.extend(category_page_list)
        xml_data = self.generate_sitemap_xml_data(recs)
        tmp_file = self.generate_tmp_xml_file(xml_data)
        self.move_tmp_file(host, username, key_file, tmp_file, remote_path, filename)
        tmp_file.close()
        return True

    def article_sitemap(self, site_model, domain, host, username, key_file, remote_path):
        day = calendar.monthrange(int(self.year), int(self.month))
        from_date = "{0}-{1}-{2}".format(self.year, self.month, "01")
        till_date = "{0}-{1}-{2}".format(self.year, self.month, day[1])
        date_obj = datetime.strptime(from_date, "%Y-%m-%d")
        month_name = date_obj.strftime("%B").lower()
        filename = ARTICLE_FILENAME.format(month_name, self.year)

        result = []
        recs = self.env[site_model].search([("date", ">=", from_date),
                                            ("date", "<=", till_date),
                                            ("published_on", "<=", datetime.now()),
                                            ("is_exported", "=", True)])

        for rec in recs:
            loc = "{0}/category/{1}/{2}/".format(domain, rec.category_id.url, rec.site_url)
            result.append({"loc": loc,
                           "lastmod": self.us_format(rec.date)})

        xml_data = self.generate_sitemap_xml_data(result)
        tmp_file = self.generate_tmp_xml_file(xml_data)
        self.move_tmp_file(host, username, key_file, tmp_file, remote_path, filename)
        tmp_file.close()
        return True

    def generate_sitemap_xml_data(self, recs):
        urlset = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        for rec in recs:
            url = etree.SubElement(urlset, "url")
            etree.SubElement(url, "loc").text = rec["loc"]
            etree.SubElement(url, "lastmod").text = rec["lastmod"]

        data = etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding="utf-8")
        return data

    def generate_tmp_xml_file(self, xml_data):
        prefix = datetime.now().strftime('%s')
        tmp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=".xml", delete=False, mode="wb+")
        tmp_file.write(xml_data)
        tmp_file.flush()

        return tmp_file

    def move_tmp_file(self, host, username, key_filename, tmp_file, path, filename):
        ssh_client = SSHClient()
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(hostname=host, username=username, key_filename=key_filename)
        sftp_client = ssh_client.open_sftp()
        local_path = tmp_file.name
        remote_path = os.path.join(path, "sitemap", filename)
        sftp_client.put(local_path, remote_path)
        sftp_client.close()
        tmp_file.close()

        return True

    def us_format(self, date):
        result = None
        if date:
            result = date.strftime("%Y-%m-%d")
        return result
