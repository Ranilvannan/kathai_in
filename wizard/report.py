from odoo import models, fields, api
from xlsxwriter import Workbook
import io
import base64


class ReportService(models.TransientModel):
    _name = "report.service"
    _description = "Report Service"

    from_date = fields.Date(string="From Date", required=1)
    till_date = fields.Date(string="Till date", required=1)
    item_ids = fields.One2many(comodel_name="report.service.item", inverse_name="report_id")

    def trigger_view_report(self):
        data = []

        recs = self.env["project.site1"].search([("date", ">=", self.from_date),
                                                 ("date", ">=", self.from_date)])

        count = 0
        for rec in recs:
            count = count + 1
            data.append((0, 0, {"s_no": count,
                                "site_url": rec.site_url,
                                "site_title": rec.site_title}))

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
    site_url = fields.Text(string="Site URL")
    site_title = fields.Text(string="Site Title")
    report_id = fields.Many2one(comodel_name="report.service", string="Report")
