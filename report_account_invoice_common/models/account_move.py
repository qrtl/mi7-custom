# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_factor(self):
        self.ensure_one()
        if self.move_type in ("out_invoice", "in_invoice"):
            return 1
        return -1
