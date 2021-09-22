from odoo.addons.delivery.models import delivery_carrier
from odoo import fields, models


class DeliveryMaster(models.Model):
    _name = "delivery.master"
    _inherit = "delivery.master"
    
    carrier_code = fields.Char("Carrier Code")
    name = fields.Char("Delivery Carrier Name")
    site_url = fields.Char("Tracking Site URL")
