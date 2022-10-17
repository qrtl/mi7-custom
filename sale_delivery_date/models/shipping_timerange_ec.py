# Copyright 2022 Quartile Limited

from odoo import fields, models


class ShippingTimerangeEc(models.Model):
    _name = "shipping.timerange.ec"
    _description = "Shipping Time Range"
    _order = "start_time"

    name = fields.Char(required=True)
    start_time = fields.Float(required=True)
    end_time = fields.Float(required=True)
