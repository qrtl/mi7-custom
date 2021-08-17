# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

from odoo.addons.queue_job.job import job


class StockPicking(models.Model):
    _inherit = "stock.picking"

    log_id = fields.Many2one("data.import.log", string="Log")
    yamato_slip_number = fields.Text(
        "Yamato Slip Number",
        help="Delivery Slip Number of Yamato Transport CO.,.",
        compute="_create_slip_number",
    )

    @job()
    def _validate_picking(self):
        self.ensure_one()
        for pack in self.pack_operation_ids:
            if pack.product_qty > 0:
                pack.write({"qty_done": pack.product_qty})
            else:
                pack.unlink()
        self.do_transfer()
        if not self.log_id.picking_ids.filtered(lambda x: x.state != "done"):
            self.log_id.sudo().write({"state": "done"})

    @api.depends('picking_ids')
    def _create_slip_number(self):
        tracking_numbers = []
        for picking in self.picking_ids:
            if picking.carrier_tracking_ref:
                tracking_numbers += [picking.carrier_tracking_ref + ",\n"]
        return tracking_numbers
