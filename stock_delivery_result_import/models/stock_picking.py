# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models
from odoo.addons.queue_job.job import job


class StockPicking(models.Model):
    _inherit = "stock.picking"

    log_id = fields.Many2one("data.import.log", string="Log")


    @job()
    def _validate_picking(self):
        self.ensure_one()
        self.action_done()
        if not self.log_id.picking_ids.filtered(lambda x: x.state != "done"):
            self.log_id.sudo().write({"state": "done"})
