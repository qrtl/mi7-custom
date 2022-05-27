# Copyright 2019-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    maker_id = fields.Many2one("product.maker", "Maker")
