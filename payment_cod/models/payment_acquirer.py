# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    is_cod = fields.Boolean("Cash on Delivery")
    amount_limit = fields.Monetary(
        help="Threshold amount - the acquirer is available when order amount is equal "
        "to or lower than the set amount.",
    )
    currency_id = fields.Many2one(related="company_id.currency_id")
    fee_product_id = fields.Many2one("product.product", string="Fee Product")
