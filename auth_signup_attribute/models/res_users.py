# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _signup_create_user(self, values):
        if "partner_id" not in values:
            if values.get("company_type") == "company":
                # A company has no date of birth. The key is dropped rather than
                # emptied because an empty string reaches the database as is:
                # 'fields.Date' does not override 'convert_to_column'.
                values.pop("birthday", None)
            elif not values.get("birthday"):
                # The 'required' attribute on the input can be bypassed.
                raise UserError(_("Please enter your date of birth."))
        return super()._signup_create_user(values)
