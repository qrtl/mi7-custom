from odoo import fields, models


class DeliveryMaster(models.Model):
    _name = "delivery.master"
    _description = "Delivery Master"

    carrier_code = fields.Char("Carrier Code")
    name = fields.Char("Delivery Carrier Name")
    site_url = fields.Char("Tracking Site URL")
