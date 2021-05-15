# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models
from odoo.addons.queue_job.job import job


class StockPicking(models.Model):
    _inherit = "stock.picking"

    log_id = fields.Many2one("data.import.log", string="Log")


    @job()
    def _assign_and_validate(self, line_num):
        self.ensure_one()
        self.action_assign()
        if self.state != "assigned":
            message = _("The delivery is not ready to be processed.")
            self.env["data.import.error"].create(
                {
                    "log_id": self.log_id.id,
                    "row_no": line_num,
                    "picking_ref": self.name,
                    "error_message": message,
                }
            )
        else:
            self.action_done()
