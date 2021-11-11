# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    is_payment_charge = fields.Boolean(
        "Is Payment Charge.",
        related="product_id.is_payment_charge",
        readonly=True,
        help="If this field is checked, this product is eligible for cash on delivery.",
    )
