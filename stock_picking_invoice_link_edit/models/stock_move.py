# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def name_get(self):
        # Manipulating with the stock move record name to show the picking, since it is
        # hard to select the move record otherwise.
        params = self._context.get("params")
        if not params or params.get("model") != "stock.picking":
            res = []
            for move in self:
                picking = move.picking_id
                product = move.product_id
                res.append(
                    (
                        move.id,
                        "%s%s%s%s>%s"
                        % (
                            picking.name and "%s/" % picking.name or "",
                            picking.origin and "%s/" % picking.origin or "",
                            product.code and "%s: " % product.code or "",
                            move.location_id.name,
                            move.location_dest_id.name,
                        ),
                    )
                )
            return res
        return super().name_get()
