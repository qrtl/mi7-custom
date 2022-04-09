# -*- coding: utf-8 -*-
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class WebsiteSale(WebsiteSale):

    def cart_content_validate(self, order):
        return []
    
    @http.route()
    def cart(self, **post):
        res = super(WebsiteSale, self).cart(**post)
        order = request.website.sale_get_order()
        res.qcontext["error_message"] = self.cart_content_validate(order)
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
        return super(WebsiteSale, self).checkout(**post)
