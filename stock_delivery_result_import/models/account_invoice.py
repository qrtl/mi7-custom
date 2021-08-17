# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    yamato_slip_number = fields.Text(
        "Yamato Slip Number",
        help="Delivery Slip Number of Yamato Transport CO.,.",
        compute="_compute_slip_number",
    )

    @api.depends("picking_ids")
    def _compute_slip_number(self):
        tracking_numbers = []
        for picking in self.picking_ids:
            if picking.carrier_tracking_ref:
                tracking_numbers += [picking.carrier_tracking_ref + ",\n"]
        return tracking_numbers
