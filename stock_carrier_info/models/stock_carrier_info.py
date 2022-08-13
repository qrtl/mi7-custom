from odoo import fields, models


class StockCarrierInfo(models.Model):
    _name = "stock.carrier.info"
    _description = "Stock Carrier Info"

    code = fields.Char("Carrier Code", required=True)
    name = fields.Char("Carrier Name", required=True)
    tracking_url = fields.Char("Tracking URL")
