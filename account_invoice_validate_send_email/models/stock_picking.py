# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    not_send_invoice = fields.Boolean(
        string="Not Auto-send Invoice",
        help="When this field is selected, the invoice that is related to this "
        "picking will be outside the scope of automated invoice email despite "
        "the settings of the linked workflow process.",
    )
