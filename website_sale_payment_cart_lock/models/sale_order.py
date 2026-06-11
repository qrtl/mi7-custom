# Copyright 2026 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

LOCK_TIMEOUT = 1800


class SaleOrder(models.Model):
    _inherit = "sale.order"

    website_cart_locked = fields.Boolean(compute="_compute_website_cart_locked")

    @api.depends("state", "transaction_ids.state", "transaction_ids.create_date")
    def _compute_website_cart_locked(self):
        threshold = fields.Datetime.now() - timedelta(seconds=LOCK_TIMEOUT)
        for order in self:
            order.website_cart_locked = order.state == "draft" and bool(
                order.sudo().transaction_ids.filtered(
                    lambda tx: tx.state in ("draft", "pending", "authorized")
                    and tx.create_date >= threshold
                )
            )

    def _get_website_cart_lock_message(self):
        self.ensure_one()
        return _(
            "This cart is currently being processed for payment. "
            "Please wait for the payment result before making changes."
        )

    def _cart_update(self, *args, **kwargs):
        self.ensure_one()
        if self.website_cart_locked:
            raise UserError(self._get_website_cart_lock_message())
        return super()._cart_update(*args, **kwargs)
