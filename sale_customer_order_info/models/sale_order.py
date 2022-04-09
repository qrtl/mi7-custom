# -*- coding: utf-8 -*-
# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_order = fields.Char("Store Order", oldname="store_order")
    customer_contact = fields.Char("Person", oldname="person")
