# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    carrier_info_name = fields.Char(
        "Delivery Carrier Name",
        help="Delivery Carrier Information for send a e-mail to customer.",
        compute="_compute_carrier_info"
    )

    carrier_info_url = fields.Char(
        "Delivery Carrier URL",
        help="Delivery Carrier's URL for tracking.",
        compute="_compute_carrier_info"
    )

    @api.multi
    def _compute_carrier_info(self):
        for invoice in self:
            picking = invoice.picking_ids[1]
            if picking.carrier_info_id:
                invoice.carrier_info_name = picking.carrier_info_id.name
                invoice.carrier_info_url = picking.carrier_info_id.site_url
