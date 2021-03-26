from odoo import models, fields, api
from xlsxwriter import Workbook
import io
import base64
from datetime import datetime

PER_PAGE = 9


class ReportService(models.TransientModel):
    _name = "report.service"
    _description = "Report Service"

    from_date = fields.Date(string="From Date", required=1)
    till_date = fields.Date(string="Till date", required=1)
    item_ids = fields.One2many(comodel_name="report.service.item", inverse_name="report_id")

    def home_page_urls(self):
        result = []
        count = self.env["project.site1"].search_count([("is_exported", ">=", True)])

        if count:
            total_page = int(count / PER_PAGE) + 1
            url = self.env["project.site1"].get_domain_url()
            for page in range(1, total_page):
                loc = "{0}turn/{1}".format(url, page)
                lastmod = datetime.now().strftime("%Y-%m-%d")
                result.append((0, 0, {"loc": loc,
                                      "lastmod": lastmod}))

        return result

    def category_page_urls(self):
        result = []
        category_ids = self.env["story.category"].search([])

        for category_id in category_ids:
            count = self.env["project.site1"].search_count([("is_exported", ">=", True),
                                                            ("category_id", "=", category_id.id)])
            print(category_id.name, count, "---")
            if count:
                total_page = int(count/PER_PAGE) + 1
                category_url = self.env["project.site1"].get_category_url(category_id)
                for page in range(1, total_page):
                    loc = "{0}turn/{1}".format(category_url, page)
                    lastmod = datetime.now().strftime("%Y-%m-%d")
                    result.append((0, 0, {"loc": loc,
                                          "lastmod": lastmod}))

        return result

    def trigger_view_report(self):
        data = []

        recs = self.env["project.site1"].search([("date", ">=", self.from_date),
                                                 ("date", ">=", self.from_date),
                                                 ("is_exported", "=", True)])

        count = 0
        for rec in recs:
            count = count + 1
            data.append((0, 0, {"s_no": count,
                                "loc": rec.get_real_url(),
                                "lastmod": rec.get_published_on_us_format()}))

        category_page_list = self.category_page_urls()
        data.extend(category_page_list)

        home_page_list = self.home_page_urls()
        data.extend(home_page_list)

        self.item_ids.unlink()
        self.item_ids = data

    def get_workbook(self):
        output = io.BytesIO()

        wb = Workbook(output, {'in_memory': True})
        ws = wb.add_worksheet()

        format1 = wb.add_format({'border': 1})

        ws.set_column(0, 0, 10)
        ws.set_column(0, 1, 30)

        headers = ['S.No', 'Site URL', 'Site Title']

        header_count = 0
        for head in headers:
            ws.write(0, header_count, head, format1)
            header_count = header_count + 1

        count = 0
        for rec in self.item_ids:
            count = count + 1
            ws.write(count, 0, rec.s_no)
            ws.write(count, 1, rec.site_url)
            ws.write(count, 2, rec.site_title)

        wb.close()
        output.seek(0)

        from_date = self.from_date.strftime("%d-%m-%Y")
        till_date = self.till_date.strftime("%d-%m-%Y")

        report_name = "Project Site 1 Report {from_date} - {till_date}.xlsx".format(from_date=from_date,
                                                                                    till_date=till_date)

        att_id = self.env["book.attachment"].create({
            "name": report_name,
            "att": base64.b64encode(output.read()),
            "description": "Project Site 1 Report"})
        return att_id

    def trigger_download_report(self):
        att_id = self.get_workbook()
        return {
            'type': 'ir.actions.act_url',
            'url': '/report_xlsx?model=book.attachment&record_id={record_id}'.format(record_id=att_id.id),
            'target': 'self',
        }


class ReportServiceItem(models.TransientModel):
    _name = "report.service.item"
    _description = "Report Service Item"

    s_no = fields.Integer(string="S.No")
    loc = fields.Text(string="URL")
    lastmod = fields.Text(string="Last Modified")
    report_id = fields.Many2one(comodel_name="report.service", string="Report")
