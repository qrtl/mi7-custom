# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_affiliate_a8_items(self):
        self.ensure_one()
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
        return affiliate_items
