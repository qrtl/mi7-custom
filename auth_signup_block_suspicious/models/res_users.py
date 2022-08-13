# Copyright 2021-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    def action_reset_password(self):
        if "http" in self.name:
            raise UserError(_("Invalid name!"))
        return super().action_reset_password()
