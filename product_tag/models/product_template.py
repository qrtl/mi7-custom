# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_tag_ids = fields.Many2many(
        "product.tag", "product_tag_product_template_rel", string="Product Tags"
    )
