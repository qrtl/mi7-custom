# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"


    def _update_vals(self, vals):
        process = self.env["sale.workflow.process"].search([("apply_to", "=", vals["order_type"])])[:1]
        if process:
            vals["workflow_process_id"] = process.id
        return vals

    @api.model
    def create(self, vals):
        if vals.get("order_type"):
            vals = self._update_vals(vals)
        return super(SaleOrder, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get("order_type"):
            vals = self._update_vals(vals)
        return super(SaleOrder, self).write(vals)
