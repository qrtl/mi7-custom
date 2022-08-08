# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    related_product_ids = fields.Many2many(
        "product.template",
        "product_related_rel",
        "src_id",
        "dest_id",
        check_company=True,
        string="Related Products",
        help="Define related products that should be preconditions for customers to "
        "purchase the product.",
    )
