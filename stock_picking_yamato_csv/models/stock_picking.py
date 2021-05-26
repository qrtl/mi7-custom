# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    yamato_carrier_code = fields.Char("Carrier Code", help="For Yamato shipping instructions.")
    is_exported = fields.Boolean("Exported")

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        if view_type == "tree":
            pick_type_id = self._context.get("default_picking_type_id")
            if (
                not pick_type_id
                or pick_type_id
                and self.env["stock.picking.type"].browse([pick_type_id]).code
                in "outgoing"
            ):
                view_id = self.env.ref("stock_picking_yamato_csv.vpicktree_outgoing").id
        return super(StockPicking, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        res.yamato_carrier_code = res.partner_id.yamato_carrier_code if res.partner_id and res.partner_id.yamato_carrier_code else res.picking_type_id.warehouse_id.yamato_carrier_code
        return res
