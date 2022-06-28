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
        required=True,
        default="b2b",
        copy=False,
    )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            self.user_type = self.partner_id.commercial_partner_id.user_type
            return
        self.user_type = False
        return

    @api.model
    def create(self, vals):
        if not vals.get("user_type", False):
            # EC orders should fall into this case unless the logic is adjusted in the
            # controller side.
            partner = self.env["res.partner"].browse(vals.get("partner_id"))
            vals["user_type"] = partner.commercial_partner_id.user_type
        if vals["user_type"] != "b2c":
            return super(SaleOrder, self).create(vals)
        # Apply the b2c sequence for b2c orders.
        if "company_id" in vals:
            self = self.with_company(vals["company_id"])
        if vals.get("name", _("New")) == _("New"):
            seq_date = None
            if "date_order" in vals:
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals["date_order"])
                )
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "sale.b2c.sequence", sequence_date=seq_date
            ) or _("New")
        return super(SaleOrder, self).create(vals)
