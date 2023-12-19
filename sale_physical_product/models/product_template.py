# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_physical = fields.Boolean(
        "Physical Product",
        help="The selection of this field affects a few different areas, such as the "
        "availability of delivery type, date and time, and the judgment of the cart "
        "being service-only or not.",
    )
