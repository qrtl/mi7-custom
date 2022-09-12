# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    affiliate_items = fields.Text(
        help="Order line list to be passed to A8 with JS-tag.",
        compute="_compute_affiliate_items",
    )

    def _compute_affiliate_items(self):
        affiliate_items = []
        for line in self.order_line:
            # TODO: Not comfortable with how default_code is used to judge the delivery.
            if line.product_id.default_code == "COD" or line.is_delivery:
                continue
            unit_price_total = line.price_unit
            if line.discount:
                unit_price_total = line.price_unit * (
                    1 - (line.discount or 0.0) / 100.0
                )
            item_dict = {
                "code": line.product_id.default_code or "",
                "price": unit_price_total,
                "quantity": line.product_uom_qty,
            }
            affiliate_items.append(item_dict)
        self.affiliate_items = affiliate_items
