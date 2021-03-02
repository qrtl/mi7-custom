# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json

from odoo.http import request
from odoo.addons.web.controllers.main import CSVExport, ExcelExport


class CSVExportInherit(CSVExport):

    # Override the base() method which is used to gather fields' values in the
    # export CSV.
    def base(self, data, token):
        params = json.loads(data)
        # When the stock.outgoing.shipment.report model is selected, remove
        # the first element in the fields list which is the External ID by
        # default.
        if params["model"] == "stock.outgoing.shipment.report":
            params["fields"].pop(0)
            data = json.dumps(params)
            report = request.env["stock.outgoing.shipment.report"]
            records = report.browse(params["ids"]) or report.search(params["domain"], offset=0, limit=False, order=False)
            records.update({
                'is_exported': True
            })
        return super(CSVExportInherit, self).base(data, token)


class ExcelExportInherit(ExcelExport):

    # Override the base() method which is used to gather fields' values in the
    # export Excel.
    def base(self, data, token):
        params = json.loads(data)
        # When the stock.outgoing.shipment.report model is selected, remove
        # the first element in the fields list which is the External ID by
        # default.
        if params["model"] == "stock.outgoing.shipment.report":
            params["fields"].pop(0)
            data = json.dumps(params)
            report = request.env["stock.outgoing.shipment.report"]
            records = report.browse(params["ids"]) or report.search(params["domain"], offset=0, limit=False, order=False)
            records.update({
                'is_exported': True
            })
        return super(ExcelExportInherit, self).base(data, token)
