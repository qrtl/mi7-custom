# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

# from odoo.exceptions import ValidationError

FIELDS_PROPERTIES = {
    # "shipping_mode": ["Char", 2],
    # "carrier_name": ["Char", 20],
    # "partner_ref": ["Char", 10],
    # "partner_zip": ["Char", 8],
    # "partner_address": ["Char", 80],
    # "product_code": ["Char", 7],
    # "product_name": ["Char", 32],
    # "case_qty": ["Float", 5],
    # "separate_qty": ["Float", 5],
    # "lot_num": ["Float", 6],
    # "lot_branch_num": ["Float", 2],
    # "delivery_division": ["Char", 1],
    # "customer_delivery_note": ["Char", 9],
    # "client_order_ref": ["Char", 30],
    # "memo": ["Char", 9],
}


class StockOutgoingShipmentReport(models.Model):
    _name = "stock.outgoing.shipment.report"

    move_id = fields.Many2one("stock.move", string="Stock Move", readonly=True,)
    name = fields.Char("Test Field")
    is_exported = fields.Boolean("Exported")

    # @api.constrains(
    #     "shipping_mode",
    #     "carrier_name",
    #     "partner_ref",
    #     "partner_zip",
    #     "partner_address",
    #     "product_code",
    #     "product_name",
    #     "case_qty",
    #     "separate_qty",
    #     "lot_num",
    #     "lot_branch_num",
    #     "delivery_division",
    #     "customer_delivery_note",
    #     "client_order_ref",
    #     "memo",
    # )
    # def _validate_field_length(self):
    #     msg = _("%s should be at most %s digit(s).")
    #     for rec in self:
    #         for field, prop in FIELDS_PROPERTIES.items():
    #             if rec[field] and len(str(rec[field])) > prop[1]:
    #                 raise ValidationError(
    #                     msg % (_(rec.fields_get(field)[field].get("string")), prop[1])
    #                 )

    # @api.constrains("case_qty", "separate_qty", "lot_num", "lot_branch_num")
    # def _validate_number_fields(self):
    #     msg = _("Only numbers are allowed for %s field.")
    #     for rec in self:
    #         for field, prop in FIELDS_PROPERTIES.items():
    #             if prop[0] == "Float":
    #                 try:
    #                     int(rec[field])
    #                 except Exception:
    #                     try:
    #                         float(rec[field])
    #                     except Exception:
    #                         raise ValidationError(
    #                             msg % _(rec.fields_get(field)[field].get("string"))
    #                         )

    _sql_constraints = [
        ("move_id_uniq", "unique(move_id)", "The stock data already exists.")
    ]
