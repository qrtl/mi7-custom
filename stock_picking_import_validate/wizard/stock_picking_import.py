# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import csv
import io
from base64 import b64decode
from datetime import datetime
from collections import OrderedDict

from odoo import _, fields, models

FIELD_KEYS = {0: "field", 1: "label", 2: "field_type", 3: "required"}
# Prepare values corresponding with the keys
FIELD_VALS = [
    ["picking_ref", "出荷指示番号!", "char", True],
]


class StockPickingImport(models.TransientModel):
    _name = "stock.picking.import"
    _inherit = "data.import.mixin"

    import_file = fields.Binary(string="File")
    file_name = fields.Char(string="File Name")

    def _get_field_defs(self):
        ordered_index = OrderedDict(sorted(FIELD_KEYS.items()))
        field_defs = []
        field_def = {}
        for field in FIELD_VALS:
            for k, v in ordered_index.iteritems():
                field_def[v] = field[k]
            field_defs.append(field_def)
        return field_defs

    def _get_picking_vals(
        self, row_dict, log, company
    ):
        return {
            "company_id": company.id,
            "picking_ref": row_dict["picking_ref"],
            "log_id": log.id,
        }

    def import_stock_picking(self):
        field_defs = self._get_field_defs()
        sheet_fields, csv_iterator, error_log = self._load_import_file("stock.picking", field_defs, ["shift-jis", "utf-8"])
        company = self.env.user.company_id
        import_error = False
        picking_vals_list = []
        for row in csv_iterator:
            row_dict, error_list = self._check_field_vals(field_defs, row, sheet_fields)
            # Create error log
            if error_list:
                import_error = True
                self.env["data.import.error"].create(
                    {
                        "log_id": error_log.id,
                        "row_no": csv_iterator.line_num,
                        "picking_ref": row_dict["picking_ref"],
                        "error_message": "\n".join(error_list),
                    }
                )
            else:
                # Append vals to list
                picking_vals = self._get_picking_vals(
                    row_dict, error_log, company
                )
                picking_vals_list.append(picking_vals)
        if not import_error:
            # Process picking validation
            for dict in picking_vals_list:
                picking_ref = dict["picking_ref"]
                picking = self.env["stock.picking"].search([("name", "=", picking_ref)])
                if picking:
                    picking.log_id = error_log
                    picking.with_delay(description=_("%s: Validate Delivery") % picking.name)._assign_and_validate(csv_iterator.line_num)
            error_log.sudo().write({"state": "done"})
        return {
            "type": "ir.actions.act_window",
            "name": _("Import Result"),
            "res_model": "data.import.log",
            "view_type": "form",
            "view_mode": "form",
            "res_id": error_log.id,
            "view_id": self.env.ref("base_data_import.data_import_log_form").id,
            "target": "current",
        }
