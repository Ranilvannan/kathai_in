from odoo import models, fields, api
from datetime import datetime
import calendar
from lxml import etree


MONTH = [("1", "January")]
YEAR = [("2021", "2021"), ("2022", "2022")]


class SitemapService(models.TransientModel):
    _name = "sitemap.service"
    _description = "Sitemap Service"

    month = fields.Selection(selection=MONTH, string="Months")
    year = fields.Selection(selection=YEAR, string="Year")

    def trigger_this_month_sitemap(self):
        year_now = datetime.now().strftime("%Y")
        month_now = datetime.now().strftime("%m")

        day = calendar.monthrange(int(year_now), int(month_now))
        from_date = "{0}-{1}-{2}".format(year_now, month_now, "01")
        till_date = "{0}-{1}-{2}".format(year_now, month_now, day[1])

        recs = self.env["project.site1"].story_page_urls(from_date, till_date)
        urlset = etree.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        for rec in recs:
            url = etree.SubElement(urlset, "url")
            etree.SubElement(url, "loc").text = rec["loc"]
            etree.SubElement(url, "lastmod").text = rec["lastmod"]
            etree.SubElement(url, "changefreq").text = "monthly"
            etree.SubElement(url, "priority").text = "0.5"

        data = etree.tostring(urlset)
        print(data)

        tree = etree.ElementTree(urlset)
        tree.write('output.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")

    def trigger_monthly_sitemap(self):
        pass

    def trigger_page_wise_sitemap(self):
        pass
