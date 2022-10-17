# Copyright 2022 Quartile Limited

from datetime import datetime, timedelta

from odoo import api, fields, models

from odoo.addons.base_timezone_converter.tools.tz_utils import convert_datetime_to_utc


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_time_id = fields.Many2one(
        "shipping.timerange.ec",
        string="Requested Delivery Time",
        tracking=True,
    )
    delivery_date = fields.Date("Requested Delivery Date", tracking=True)

    @api.model
    def _get_delivery_date(self, delivery_date):
        delivery_date = "%s 09:00:00" % (delivery_date)
        commitment_date = convert_datetime_to_utc(delivery_date, self.env.user.tz)
        whs_ship_days = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("warehouse.shipping.delay", default=0)
        )
        return commitment_date - timedelta(days=int(whs_ship_days))

    def write(self, vals):
        if "delivery_date" not in vals:
            return super().write(vals)
        if not vals.get("delivery_date"):
            vals["commitment_date"] = False
            return super().write(vals)
        for order in self:
            delivery_date = vals.get("delivery_date") or order.delivery_date
            vals["commitment_date"] = self._get_delivery_date(delivery_date)
            return super(SaleOrder, order).write(vals)
