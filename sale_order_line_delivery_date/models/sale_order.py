# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    delivery_date = fields.Date(
        help="Delivery date for internal reference only. Input value does not affect "
        "anything.",
    )
