# -*- coding: utf-8 -*-
# Copyright 2020-2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import csv
import io
from base64 import b64decode
from datetime import datetime
from collections import OrderedDict

from odoo import _, fields, models
from odoo.exceptions import UserError


class DataImport(models.TransientModel):
    _name = "data.import"

    import_file = fields.Binary(string="File")
    file_name = fields.Char(string="File Name")

    def import_data(self):
        return

    def _create_import_log(self, model_name):
        model = self.env["ir.model"].search([("model", "=", model_name)])
        ir_attachment = self.env["ir.attachment"].create(
            {
                "name": self.file_name,
                "datas": self.import_file,
                "datas_fname": self.file_name,
            }
        )
        import_log = self.env["data.import.log"].create(
            {
                "input_file": ir_attachment.id,
                "import_user_id": self.env.user.id,
                "import_date": datetime.now(),
                "state": "failed",
                "model_id": model.id,
            }
        )
        return import_log
    
    def _get_field_defs(self, FIELD_KEYS, FIELD_VALS):
        ordered_index = OrderedDict(sorted(FIELD_KEYS.items()))
        field_defs = []
        field_def = {}
        for field in FIELD_VALS:
            for k, v in ordered_index.iteritems():
                field_def[v] = field[k]
            field_defs.append(field_def)
        return field_defs

    def _load_import_file(self, field_defs, encodings=["utf-8"]):
        """We assume that there is a header line in the imported CSV.
        """
        csv_data = b64decode(self.import_file)
        for encoding in encodings:
            try:
                csv_iterator = csv.reader(
                    io.StringIO(csv_data.decode(encoding)), delimiter=","
                )
                sheet_fields = next(csv_iterator)
                # Once deciding is successful, we revert the strings to utf-8
                sheet_fields = [field.encode("utf-8") for field in sheet_fields]
                break
            except Exception:
                pass
        if not sheet_fields:
            raise UserError(_("Invalid file!"))
        missing_columns = list(
            {field_def["label"] for field_def in field_defs} - set(sheet_fields)
        )
        if missing_columns:
            raise UserError(
                _("Following columns are missing: \n %s" % ("\n".join(missing_columns)))
            )
        return sheet_fields, csv_iterator

    def _check_value_type(self, field_type, value, date_formats):
        # numeric fields
        if field_type == "float":
            try:
                float(value)
                return False
            except Exception:
                return field_type
        # date fields
        elif field_type == "date":
            date = False
            for date_format in date_formats:
                try:
                    date = datetime.strptime(value, date_format)
                    break
                except Exception:
                    pass
            return field_type if not date else False

    def _check_field_vals(self, field_defs, row, sheet_fields, date_formats=["%Y-%m-%d", "%Y/%m/%d"]):
        error_list = []
        row_dict = {}
        for field_def in field_defs:
            field = field_def["field"]
            label = field_def["label"]
            field_type = field_def["field_type"]
            required = field_def["required"]
            value = row[sheet_fields.index(label)]
            if required and not value:
                error_list.append(_("%s is missing." % label))
            else:
                row_dict[field] = value
                errored_type = self._check_value_type(field_type, value, date_formats)
                if errored_type:
                    message = _("Unexpected value for %s (%s)") % (label, errored_type)
                    error_list.append(message)
        return row_dict, error_list

    def _action_open_import_log(self, import_log):
        return {
            "type": "ir.actions.act_window",
            "name": _("Import Result"),
            "res_model": "data.import.log",
            "view_type": "form",
            "view_mode": "form",
            "res_id": import_log.id,
            "view_id": self.env.ref("base_data_import.data_import_log_form").id,
            "target": "current",
        }
