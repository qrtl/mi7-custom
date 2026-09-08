# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.http import request


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _signup_create_user(self, values):
        # Standard signup keeps only login, name and password, so the values
        # posted by this module are read back from the request. They are absent
        # for a signup that does not come from its form, such as an invitation
        # or an OAuth provider, which is then left untouched.
        params = request.params if request else {}
        if "company_type" in params:
            values["company_type"] = params["company_type"]
            if params["company_type"] == "company":
                # A company has no date of birth. The key is dropped rather than
                # emptied because an empty string reaches the database as is:
                # 'fields.Date' does not override 'convert_to_column'.
                values.pop("birthday", None)
            elif not params.get("birthday"):
                raise UserError(_("Please enter your date of birth."))
            else:
                values["birthday"] = params["birthday"]
        return super()._signup_create_user(values)
