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

    def _load_import_file(self, IMPORT_FIELDS, encoding_list=["utf-8"]):
        """We assume that there is a header line in the imported CSV.
        """
        csv_data = b64decode(self.import_file)
        for encoding in encoding_list:
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
            {field[1] for field in IMPORT_FIELDS} - set(sheet_fields)
        )
        if missing_columns:
            raise UserError(
                _("Following columns are missing: \n %s" % ("\n".join(missing_columns)))
            )

        # for encoding in encoding_list:
        #     try:
        #         csv_iterator = csv.reader(
        #             io.StringIO(csv_data.decode(encoding)), delimiter=","
        #         )
        #         sheet_fields = next(csv_iterator)
        #         break
        #     except Exception:
        #         pass
        # if not sheet_fields:
        #     raise UserError(_("Invalid file!"))
        # # fields = {field[1] for field in IMPORT_FIELDS}
        # # for f in fields:
        # #     f.encode(encoding)
        # missing_columns = list(
        #     {field[1].encode(encoding) for field in IMPORT_FIELDS} - set(sheet_fields)
        # )
        # if missing_columns:
        #     fields = [field.decode(encoding) for field in missing_columns]
        #     raise UserError(
        #         _("Following columns are missing: \n %s" % ("\n".join(fields)))
        #     )
        model = self.env["ir.model"].search([("model", "=", "account.payment.import")])
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
