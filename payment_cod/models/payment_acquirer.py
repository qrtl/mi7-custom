# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    is_cod = fields.Boolean("Cash on Delivery")
    amount_limit = fields.Monetary(
        help="Threshold amount - the acquirer is available when order amount is equal "
        "to or lower than the set amount.",
    )
    currency_id = fields.Many2one(related="company_id.currency_id")
    fee_product_id = fields.Many2one("product.product", string="Fee Product")

    @api.depends("provider", "is_cod")
    def _compute_view_configuration_fields(self):
        super()._compute_view_configuration_fields()
        self.filtered(lambda acq: acq.provider == "transfer" and acq.is_cod).write(
            {
                "show_pre_msg": True,
                "show_pending_msg": False,
                "show_done_msg": True,
            }
        )
        return
