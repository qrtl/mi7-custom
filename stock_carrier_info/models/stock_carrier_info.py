from odoo import fields, models


class DeliveryMaster(models.Model):
    _name = "stock.carrier.info"
    _description = "Stock Carrier Info"

    carrier_code = fields.Char("Carrier Code")
    name = fields.Char("Delivery Carrier Name")
    site_url = fields.Char("Tracking Site URL")
