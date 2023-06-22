# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api

from odoo.addons.purchase.models.purchase import PurchaseOrder

# For purchase order amount total calculation. This affects the order total
# presentation of orders, for example.
# _compute_amount() of purchase.order.line may also require the same arrangement in case
# tax rounding is configured to be done per line, which does not apply to the use in
# Japan.


@api.depends("order_line.price_total")
def _new_amount_all(self):
    for order in self:
        amount_untaxed = amount_tax = 0.0
        for line in order.order_line:
            line._compute_amount()
            amount_untaxed += line.price_subtotal
            amount_tax += line.price_tax
        currency = (
            order.currency_id
            or order.partner_id.property_purchase_currency_id
            or self.env.company.currency_id
        )
        # Without this, rounding_method="DOWN" may be unexpectedly applied to amount_untaxed.
        currency = currency.with_context(rounding_method="HALF-UP")
        order.amount_untaxed = currency.round(amount_untaxed)
        if self.env.company.need_tax_round_down:
            currency = currency.with_context(rounding_method="DOWN")
        order.amount_tax = currency.round(amount_tax)
        order.amount_total = order.amount_untaxed + order.amount_tax


def post_load_hook():
    PurchaseOrder._amount_all = _new_amount_all
