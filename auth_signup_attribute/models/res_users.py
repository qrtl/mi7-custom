# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.http import request


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def _signup_create_user(self, values):
        # Standard signup keeps only login, name and password, so the posted
        # attributes are read back from the request. They are absent for an
        # invitation or an OAuth signup, which is then left untouched.
        params = request.params if request else {}
        birthday = False
        if "company_type" in params:
            values["company_type"] = params["company_type"]
            if params["company_type"] != "company":
                if not params.get("birthday"):
                    error = _("Please enter your date of birth.")
                    # The controller discards the message, so the template
                    # picks the reason back up from here.
                    params["signup_attribute_error"] = error
                    raise UserError(error)
                birthday = params["birthday"]
        # 'hr' redefines 'birthday' on res.users as a related field of the
        # employee, shadowing the one delegated from the partner and discarding
        # the value without error, so the partner is written directly.
        values.pop("birthday", None)
        user = super()._signup_create_user(values)
        if birthday:
            user.partner_id.birthday = birthday
        return user
