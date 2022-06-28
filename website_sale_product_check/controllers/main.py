# Copyright 2022 Quartile Limited

from odoo import http
from odoo.http import request

from odoo.addons.website.models.website import slug
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def product_validate(self, product):
        return []

    @http.route()
    def product(self, product, category="", search="", **kwargs):
        res = super(WebsiteSale, self).product(
            product, category=category, search=search, **kwargs
        )
        res.qcontext.setdefault("error_message", [])
        error_message = self.product_validate(product)
        if error_message:
            res.qcontext["error_message"].extend(error_message)
        return res

    @http.route()
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        product = request.env["product.product"].sudo().browse(int(product_id))
        error_message = self.product_validate(product.product_tmpl_id)
        if error_message:
            return request.redirect("/shop/product/%s" % slug(product.product_tmpl_id))
        return super(WebsiteSale, self).cart_update(
            product_id, add_qty=add_qty, set_qty=set_qty, **kw
        )
