# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_exported = fields.Boolean("Exported")

    @api.multi
    def generate_stock_picking_export_report(self):
        if any(self.mapped("is_exported")):
            raise UserError(
                _(
                    "Following records have been exported before. Please uncheck 'Exported' if re-export is needed."
                )
            )
        report_obj = self.env["stock.picking.export.report"]
        for picking in self:
            company = picking.company_id
            order = picking.sale_id
            moves = picking.move_lines
            report_obj.search(
                [("move_id", "in", moves.ids), ("is_exported", "=", False)]
            ).unlink()
            for move in moves:
                # partner = move.picking_partner_id
                # product = move.product_id
                vals = {
                    "move_id": move.id,
                    "picking_id": picking.id,
                    "request_categ": "1",
                    "shipper_code": company.shipper_code,
                    "ship_categ": "10", #TODO check requirement
                    "carrier_code": "YTC01", # Fixed as Yamato
                    "whs_code": "S001", # Fixed
                    "dlv_rqstd_time_categ": order.delivery_time_id and order.delivery_time_id.dlv_rqstd_time_categ or "",
                    "dlv_service_categ": "20" if order.is_cod else "10",
                    "amount": int(order.amount_untaxed),
                    "b2_consump_amt": int(order.amount_tax),
                    # "shipping_mode": order.carrier_id.shipping_mode,
                    # "carrier_name": order.carrier_id.name[:20]
                    # if order and order.carrier_id and len(order.carrier_id.name) > 20
                    # else order and order.carrier_id and order.carrier_id.name or False,
                    # "product_code": product.default_code[:7]
                    # if product and product.default_code and len(product.default_code) > 7
                    # else product and product.default_code,
                    # "product_name": product.name[:32]
                    # if product and len(product.name) > 32
                    # else product and product.name,
                    # "client_order_ref": move.sale_line_id
                    # and move.sale_line_id.client_order_ref,
                    # "memo": move.note[:9]
                    # if move.note and len(move.note) > 9
                    # else move.note,
                }
                # exist_data_line = exist_data_lines.filtered(lambda r: r.move_id == move)
                # try:
                #     self.env["stock.picking.export.report"].create(vals)
                # except Exception:
                #     if exist_data_line and not exist_data_line.is_exported:
                #         exist_data_line.update(vals)
                report_obj.create(vals)
            picking.update({"is_exported": True})
        return self.env.ref(
            "stock_picking_export_report.action_stock_picking_export_report"
        ).read()[0]
