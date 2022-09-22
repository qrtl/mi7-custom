# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductWishlist(models.Model):
    _inherit = "product.wishlist"

    def _add_to_wishlist(
        self, pricelist_id, currency_id, website_id, price, product_id, partner_id=False
    ):
        wish = super()._add_to_wishlist(
            pricelist_id=pricelist_id,
            currency_id=currency_id,
            website_id=website_id,
            price=price,
            product_id=product_id,
            partner_id=partner_id,
        )
        wish["stock_notification"] = False
        return wish
