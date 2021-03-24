from odoo import http
from odoo.http import request
import base64


class ExcelExporter(http.Controller):

    @http.route('/report_xlsx', type='http', auth='user')
    def check_1(self):
        model = request.params.get('model')
        record_id = request.params.get('record_id')
        obj = request.env[model].search([("id", "=", record_id)])
        output = base64.b64decode(obj.att)

        return request.make_response(output, headers=[
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            ('Content-Disposition', 'attachment; filename={filename}.xlsx'.format(filename=obj.name)),
        ])
