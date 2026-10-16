# Copyright 2026 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _deactivate_portal_account(self):
        # The user must be archived first, as a partner linked to an active user
        # cannot be archived.
        self.write({"active": False})
        self.partner_id._anonymize_for_account_deletion()
        self.unlink()
