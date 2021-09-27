from odoo import fields, models


class DeliveryMaster(models.Model):
    _name = "stock.carrier.info"
    _description = "Stock Carrier Info"

    picking_ids = fields.One2many(
        "stock.picking", "carrier_info_id", string="Picking ID"
    )
    carrier_code = fields.Char("Carrier Code")
    name = fields.Char("Delivery Carrier Name")
    site_url = fields.Char("Tracking Site URL")
