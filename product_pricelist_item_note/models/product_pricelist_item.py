# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductPriceListItem(models.Model):
    _inherit = "product.pricelist.item"

    note = fields.Text("Comment", oldname="comment")
