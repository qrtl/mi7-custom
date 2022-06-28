# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    def product_validate(self, product):
        return []

    def _prepare_product_values(self, product, category, search, **kwargs):
        values = super()._prepare_product_values(product, category, search, **kwargs)
        values["error_message"] = self.product_validate(product)
        return values

    @http.route()
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        product = request.env["product.product"].sudo().browse(int(product_id))
        error_message = self.product_validate(product.product_tmpl_id)
        if error_message:
            # TODO: Check if commented way of redirection is more desirable.
            # return request.redirect(_build_url_w_params("/shop/%s" % slug(product.product_tmpl_id), request.params), code=301)  # noqa
            return request.redirect("/shop/product/%s" % slug(product.product_tmpl_id))
        return super().cart_update(product_id, add_qty=add_qty, set_qty=set_qty, **kw)
