# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Product(models.Model):
    _inherit = "product.product"

    def get_product_multiline_description_sale(self):
        """
        Returns product's display name or standard description
        based on the 'use_description_sale'.
        """
        if not self.use_description_sale:
            return self.display_name
        return super().get_product_multiline_description_sale()
