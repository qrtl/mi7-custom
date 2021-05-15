# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import csv
import io
from base64 import b64decode
from datetime import datetime

from odoo import _, fields, models
# from odoo.exceptions import UserError

IMPORT_FIELDS = [
    ["picking_ref", "出荷指示番号", "char"],
]


class StockPickingImport(models.TransientModel):
    _name = "stock.picking.import"
    _inherit = "data.import.mixin"

    import_file = fields.Binary(string="File")
    file_name = fields.Char(string="File Name")

    def _get_picking_vals(
        self, row_dict, log, company
    ):
        return {
            "company_id": company.id,
            "picking_ref": row_dict["picking_ref"],
            "log_id": log.id,
        }

    def import_stock_picking(self):
        sheet_fields, csv_iterator, error_log = self._load_import_file(IMPORT_FIELDS, ["shift-jis", "utf-8"])
        model = "stock.picking"
        company = self.env.user.company_id
        import_error = False
        picking_vals_list = []
        for row in csv_iterator:
            row_dict, error_list = self._check_field_vals(row, sheet_fields)
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

    #TODO Move this method to base_import_log
    def _check_field_vals(self, row, sheet_fields):
        error_list = []
        row_dict = {}
        for field in IMPORT_FIELDS:
            field_key = field[0]
            field_value = row[sheet_fields.index(field[1])]
            field_type = field[2]
            row_dict[field_key] = field_value
            # missing field value
            if not field_value:
                error_list.append(_("%s is required." % field[1]))
            # numeric fields
            elif field_type == "float":
                try:
                    row_dict[field_key] = float(field_value)
                except Exception:
                    row_dict[field_key] = 0.0
                    error_list.append(_("%s only accepts numeric value." % field[1]))
            # date fields
            elif field_type == "date":
                try:
                    datetime.strptime(field_value, "%Y/%m/%d")
                except Exception:
                    error_list.append(_("Incorrect date format."))
        return row_dict, error_list
