# Copyright 2021-2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _get_workflow_process(self, user_type):
        return self.env["sale.workflow.process"].search([("apply_to", "=", user_type)])[
            :1
        ]

    @api.model
    def create(self, vals):
        order = super().create(vals)
        if not order.user_type:
            return order
        process = self._get_workflow_process(order.user_type)
        if process:
            order.workflow_process_id = process.id
        return order

    def write(self, vals):
        if not vals.get("user_type"):
            return super().write(vals)
        process = self._get_workflow_process(vals.get("user_type"))
        if process:
            vals["workflow_process_id"] = process.id
        return super().write(vals)
