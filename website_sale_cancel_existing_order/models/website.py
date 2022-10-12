# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Website(models.Model):
    _inherit = "website"

    def sale_get_order(
        self,
        force_create=False,
        code=None,
        update_pricelist=False,
        force_pricelist=False,
    ):
        order = super().sale_get_order(
            force_create=force_create,
            code=code,
            update_pricelist=update_pricelist,
            force_pricelist=force_pricelist,
        )
        public_user = self.env.ref("base.public_user", raise_if_not_found=False)
        public_partner = public_user.partner_id
        if order and order.partner_id != public_partner:
            existing_orders = (
                self.env["sale.order"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", order.partner_id.id),
                        ("website_id", "=", order.website_id.id),
                        ("state", "=", "draft"),
                        ("id", "!=", order.id),
                    ]
                )
            )
            if existing_orders:
                existing_orders.action_cancel()
        return order
