# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ShippingTimerangeEc(models.Model):
    _inherit = "shipping.timerange.ec"

    dlv_rqstd_time_categ = fields.Char("Delivery Time Category", required=True, help="This field is used for shipping instruction data export.")
