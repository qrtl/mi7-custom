# Copyright 2019-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductMaker(models.Model):
    _name = "product.maker"

    name = fields.Char("Maker Name")
