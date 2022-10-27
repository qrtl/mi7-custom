# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # For purchase order amount total calculation. This affects the order total
    # presentation of orders, for example.
    # _compute_amount() of purchase.order.line may also require the same arrangemtn in case
    # tax rounding is configured to be done per line, which does not apply to the use in
    # Japan.
    def _amount_all(self):
        if self.env.company.need_tax_round_down:
            self = self.with_context(rounding_method="DOWN")
        return super()._amount_all()

    # For purchase order form and report total presentation.
    def _compute_tax_totals_json(self):
        if self.env.company.need_tax_round_down:
            self = self.with_context(rounding_method="DOWN")
        return super()._compute_tax_totals_json()
