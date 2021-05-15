# -*- coding: utf-8 -*-
# Copyright 2020-2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import csv
import io
from base64 import b64decode
from datetime import datetime

from odoo import _, models
from odoo.exceptions import UserError


class DataImportMixin(models.AbstractModel):
    _name = "data.import.mixin"

    def _load_import_file(self, model_name, field_defs, encodings=["utf-8"]):
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
        model = self.env["ir.model"].search([("model", "=", model_name)])
        ir_attachment = self.env["ir.attachment"].create(
            {
                "name": self.file_name,
                "datas": self.import_file,
                "datas_fname": self.file_name,
            }
        )
        error_log = self.env["data.import.log"].create(
            {
                "input_file": ir_attachment.id,
                "import_user_id": self.env.user.id,
                "import_date": datetime.now(),
                "state": "failed",
                "model_id": model.id,
            }
        )
        return sheet_fields, csv_iterator, error_log

    def _check_field_vals(self, field_defs, row, sheet_fields, date_formats=["%Y-%m-%d", "%Y/%m/%d"]):
        error_list = []
        row_dict = {}
        for field_def in field_defs:
            field = field_def["field"]
            label = field_def["label"]
            value = row[sheet_fields.index(label)]
            field_type = field_def["field_type"]
            row_dict[field] = value
            # missing field value
            if not value:
                error_list.append(_("%s is required." % label))
            # numeric fields
            elif field_type == "float":
                try:
                    row_dict[field] = float(value)
                except Exception:
                    row_dict[field] = 0.0
                    error_list.append(_("%s only accepts numeric value." % label))
            # date fields
            elif field_type == "date":
                date = False
                for date_format in date_formats:
                    try:
                        date = datetime.strptime(value, date_format)
                        break
                    except Exception:
                        pass
                if not date:
                    error_list.append(_("Incorrect date format: %s" % label))
        return row_dict, error_list
