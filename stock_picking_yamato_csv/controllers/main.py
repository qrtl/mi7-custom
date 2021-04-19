# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# import csv
import json
# from cStringIO import StringIO

from odoo.http import request

from odoo.addons.web.controllers.main import CSVExport, ExcelExport


class CSVExportInherit(CSVExport):

    # def from_data(self, fields, rows):
    #     # Overriding the standard method to adjust the encoding.
    #     # encoding = "utf-8"
    #     # params = json.loads(data)
    #     # if params["model"] == "stock.picking.export.report":
    #     #     encoding = "shift_jisx0213"
    #     encoding = self._context.get("encoding") or "utf-8"

    #     fp = StringIO()
    #     writer = csv.writer(fp, quoting=csv.QUOTE_ALL)

    #     # writer.writerow([name.encode('utf-8') for name in fields])
    #     writer.writerow([name.encode(encoding) for name in fields])

    #     for data in rows:
    #         row = []
    #         for d in data:
    #             if isinstance(d, unicode):
    #                 try:
    #                     # d = d.encode('utf-8')
    #                     d = d.encode(encoding)
    #                 except UnicodeError:
    #                     pass
    #             if d is False: d = None

    #             # Spreadsheet apps tend to detect formulas on leading =, + and -
    #             if type(d) is str and d.startswith(('=', '-', '+')):
    #                 d = "'" + d

    #             row.append(d)
    #         writer.writerow(row)

    #     fp.seek(0)
    #     data = fp.read()
    #     fp.close()
    #     return data

    # Override the base() method which is used to gather fields' values in the
    # export CSV.
    def base(self, data, token):
        params = json.loads(data)
        # When the stock.picking.export.report model is selected, remove
        # the first element in the fields list which is the External ID by
        # default.
        if params["model"] == "stock.picking.export.report":
            params["fields"].pop(0)
            data = json.dumps(params)
            report = request.env["stock.picking.export.report"]
            records = report.browse(params["ids"]) or report.search(
                params["domain"], offset=0, limit=False, order=False
            )
            records.update({"is_exported": True})
            # self = self.with_context(encoding="shift_jisx0213")
        # return super(CSVExportInherit, self).base(data, token)
        return super(CSVExportInherit, self).base(data, token)


class ExcelExportInherit(ExcelExport):

    # Override the base() method which is used to gather fields' values in the
    # export Excel.
    def base(self, data, token):
        params = json.loads(data)
        # When the stock.picking.export.report model is selected, remove
        # the first element in the fields list which is the External ID by
        # default.
        if params["model"] == "stock.picking.export.report":
            params["fields"].pop(0)
            data = json.dumps(params)
            report = request.env["stock.picking.export.report"]
            records = report.browse(params["ids"]) or report.search(
                params["domain"], offset=0, limit=False, order=False
            )
            records.update({"is_exported": True})
        return super(ExcelExportInherit, self).base(data, token)
