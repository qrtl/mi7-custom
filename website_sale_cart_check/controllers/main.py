# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def cart_content_validate(self, order):
        return []

    @http.route()
    def cart(self, access_token=None, revive="", **post):
        res = super().cart(access_token=access_token, revive=revive, **post)
        order = request.website.sale_get_order()
        res.qcontext.setdefault("error_message", [])
        error_message = self.cart_content_validate(order)
        if error_message:
            res.qcontext["error_message"].extend(error_message)
        return res

    @http.route()
    def checkout(self, **post):
        order = request.website.sale_get_order()
        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection
        if self.cart_content_validate(order):
            # i.e. there is some error.
            return request.redirect("/shop/cart")
        return super().checkout(**post)
