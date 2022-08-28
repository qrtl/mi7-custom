# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_cod = fields.Boolean("Cash on Delivery", compute="_compute_is_cod")

    def _compute_is_cod(self):
        for order in self:
            if order.order_line.filtered(lambda x: x.product_id.default_code == "COD"):
                order.is_cod = True
