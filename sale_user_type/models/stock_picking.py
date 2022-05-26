# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        origin = vals.get("origin", False)
        if origin:
            order = self.env["sale.order"].search([("name", "=", origin)])
            if order.user_type == "b2c":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("picking.b2c.sequence") or "/"
                )
        return super(StockPicking, self).create(vals)
