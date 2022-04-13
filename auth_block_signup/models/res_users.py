# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, models
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    def action_reset_password(self):
        if "http" in self.name:
            raise UserError(_("Invalid name!"))
        super(ResUsers, self).action_reset_password()
