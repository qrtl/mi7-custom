# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    has_physical_product = fields.Boolean(
        "Physical Product", compute="_compute_has_physical_product"
    )

    def _compute_has_physical_product(self):
        for order in self:
            order.has_physical_product = False
            if order.order_line.filtered(lambda x: x.product_id.is_physical):
                order.has_physical_product = True
