# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, _

from odoo.addons.website.controllers import form


class WebsiteForm(form.WebsiteForm):
    def insert_record(self, request, model, values, custom, meta=None):
        record_id = super().insert_record(request, model, values, custom, meta=meta)
        if custom or meta and model.website_form_default_field_id:
            record = request.env[model.model].with_user(SUPERUSER_ID).browse(record_id)
            default_field = model.website_form_default_field_id
            if _("Other Information:") in record[default_field.name]:
                values = {
                    "body": record[default_field.name],
                    "model": model.model,
                    "message_type": "comment",
                    "res_id": record.id,
                }
                request.env["mail.message"].with_user(SUPERUSER_ID).create(values)
        return record_id
