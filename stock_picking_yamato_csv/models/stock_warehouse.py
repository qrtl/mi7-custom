# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    yamato_carrier_code = fields.Char(
        "Carrier Code", help="Default Carrier Code for Yamato shipping instructions."
    )
    yamato_shipper_code = fields.Char("Shipper Code")
