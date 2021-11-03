# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockCarrierInfo(models.Model):
    _inherit = "stock.carrier.info"

    is_dummy = fields.Boolean(
        "Dummy Carrier",
        help="If selected, the carrier info will be ignored in email content "
        "preparation at the invoice validation.",
    )
