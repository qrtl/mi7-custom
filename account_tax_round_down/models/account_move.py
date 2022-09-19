# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    # For journal entries
    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        self.ensure_one()
        if self.company_id.need_tax_round_down:
            self = self.with_context(rounding_method="DOWN")
        return super()._recompute_tax_lines(
            recompute_tax_base_amount=recompute_tax_base_amount
        )

    # For invoice form and print total presentation.
    # Extending _get_tax_totals() would also work for invoices, however not for sales
    # orders. Therefore _compute_tax_totals_json() is extended for consistency reason.
    def _compute_tax_totals_json(self):
        if self.env.company.need_tax_round_down:
            self = self.with_context(rounding_method="DOWN")
        return super()._compute_tax_totals_json()
