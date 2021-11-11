# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_payment_charge = fields.Boolean(
        "Is Payment Charge.",
        help="If this product is eligible for cash on delivery, please check here.",
    )
