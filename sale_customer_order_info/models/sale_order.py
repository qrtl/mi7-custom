# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    customer_order = fields.Char()
    customer_contact = fields.Char()
