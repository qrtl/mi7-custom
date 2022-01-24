# -*- coding: utf-8 -*-
# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # We are not doing related="partner_id.user_type" here on purpose to isolate the
    # field value from the partner attribute.
    user_type = fields.Selection(
        [("b2c", "B2C"), ("b2b", "B2B")],
        string="User Type",
        required=True,
        default="b2b",
        oldname="order_type",
    )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self.user_type = self.partner_id.user_type if self.partner_id else False

    @api.model
    def create(self, vals):
        if not vals.get("user_type", False):
            # EC orders should fall into this case unless the logic is adjusted in the
            # controller side.
            partner = self.env["res.partner"].browse(vals.get("partner_id"))
            vals["user_type"] = partner.user_type
        if vals["user_type"] != "b2c":
            return super(SaleOrder, self).create(vals)
        # Apply the b2c sequence for b2c orders.
        if vals.get("name", _("New")) == _("New"):
            if "company_id" in vals:
                vals["name"] = self.env["ir.sequence"].with_context(
                    force_company=vals["company_id"]
                ).next_by_code("sale.b2c.sequence") or _("New")
            else:
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "sale.b2c.sequence"
                ) or _("New")
        return super(SaleOrder, self).create(vals)
