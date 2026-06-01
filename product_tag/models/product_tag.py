# Copyright Odoo S.A.
# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from random import randint

from odoo import fields, models


class ProductTag(models.Model):
    _name = "product.tag"
    _description = "Product Tag"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char("Tag Name", required=True, translate=True)
    color = fields.Integer(default=_get_default_color)
    product_template_ids = fields.Many2many(
        "product.template", "product_tag_product_template_rel"
    )

    _sql_constraints = [
        ("name_uniq", "unique (name)", "Tag name already exists !"),
    ]
