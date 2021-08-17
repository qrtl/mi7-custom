# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

from odoo.addons.queue_job.job import job


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    yamato_slip_number = fields.Text(
        "Yamato Slip Number",
        help="Delivery Slip Number of Yamato Transport CO.,.",
        compute="_compute_yamato_slip_number",
    )

    @job()
    def _compute_yamato_slip_number(self):
        for invoice in self:
            tracking_numbers = ""
            for picking in invoice.picking_ids:
                if picking.carrier_tracking_ref:
                    tracking_numbers += picking.carrier_tracking_ref + ",\n"
            invoice.yamato_slip_number = tracking_numbers
