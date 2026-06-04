# Copyright 2026 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    website_cart_locked = fields.Boolean(string="Website Cart Locked", copy=False)
    website_cart_lock_date = fields.Datetime(
        string="Website Cart Lock Date", copy=False, readonly=True
    )

    def _get_website_cart_lock_message(self):
        self.ensure_one()
        return _(
            "This cart is currently being processed for payment. Please wait for the payment result before making changes."
        )

    def _is_website_cart_locked(self):
        self.ensure_one()
        return self.website_cart_locked and self.state == "draft"

    def action_lock_website_cart(self):
        orders = self.filtered(lambda so: so.state == "draft" and not so.website_cart_locked)
        if orders:
            orders.write(
                {
                    "website_cart_locked": True,
                    "website_cart_lock_date": fields.Datetime.now(),
                }
            )

    def action_unlock_website_cart(self):
        orders = self.filtered("website_cart_locked")
        if orders:
            orders.write(
                {
                    "website_cart_locked": False,
                    "website_cart_lock_date": False,
                }
            )

    def action_unlock_website_cart_manually(self):
        self.action_unlock_website_cart()

    def _cart_update(
        self,
        product_id=None,
        line_id=None,
        add_qty=0,
        set_qty=0,
        display=True,
        product_custom_attribute_values=None,
        no_variant_attribute_values=None,
        **kwargs,
    ):
        self.ensure_one()
        if self._is_website_cart_locked():
            raise UserError(self._get_website_cart_lock_message())
        return super()._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            display=display,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            **kwargs,
        )
