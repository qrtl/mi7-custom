# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _need_round_down(self):
        return False

    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        if self._need_round_down():
            self = self.with_context(rounding_method="DOWN")
        return super()._recompute_tax_lines(
            recompute_tax_base_amount=recompute_tax_base_amount
        )
