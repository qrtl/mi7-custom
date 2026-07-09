# Copyright 2026 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, fields, http
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request

from odoo.addons.website_sale.controllers.main import (
    PaymentPortal as WebsiteSalePaymentPortal,
    WebsiteSale as WebsiteSaleController,
)


class WebsiteSale(WebsiteSaleController):
    def _get_cart_lock_message(self, order):
        return order._get_website_cart_lock_message()

    def _is_cart_locked(self, order):
        return bool(order and order.website_cart_locked)

    def _get_locked_cart_response(self, order, line_id=None):
        message = self._get_cart_lock_message(order)
        quantity = 0
        if line_id:
            order_line = order.order_line.filtered(
                lambda line: line.id == int(line_id)
            )[:1]
            quantity = order_line.product_uom_qty if order_line else 0
        return {
            "quantity": quantity,
            "cart_quantity": order.cart_quantity,
            "warning": message,
            "website_sale.cart_lines": request.env["ir.ui.view"]._render_template(
                "website_sale.cart_lines",
                {
                    "website_sale_order": order,
                    "date": fields.Date.today(),
                    "suggested_products": order._cart_accessories(),
                },
            ),
            "website_sale.short_cart_summary": request.env[
                "ir.ui.view"
            ]._render_template(
                "website_sale.short_cart_summary",
                {
                    "website_sale_order": order,
                },
            ),
        }

    @http.route()
    def cart(self, access_token=None, revive="", **post):
        response = super().cart(access_token=access_token, revive=revive, **post)
        order = request.website.sale_get_order()
        if hasattr(response, "qcontext") and self._is_cart_locked(order):
            response.qcontext["cart_locked_message"] = self._get_cart_lock_message(
                order
            )
        return response

    @http.route()
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        order = request.website.sale_get_order()
        if self._is_cart_locked(order):
            return request.redirect("/shop/cart")
        return super().cart_update(product_id, add_qty=add_qty, set_qty=set_qty, **kw)

    @http.route()
    def cart_update_json(
        self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kw
    ):
        order = request.website.sale_get_order()
        if self._is_cart_locked(order):
            return self._get_locked_cart_response(order, line_id=line_id)
        return super().cart_update_json(
            product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            display=display,
            **kw,
        )

    @http.route()
    def checkout(self, **post):
        order = request.website.sale_get_order()
        if self._is_cart_locked(order):
            return request.redirect("/shop/cart")
        return super().checkout(**post)

    @http.route()
    def shop_payment(self, **post):
        order = request.website.sale_get_order()
        if self._is_cart_locked(order):
            return request.redirect("/shop/cart")
        return super().shop_payment(**post)


class PaymentPortal(WebsiteSalePaymentPortal):
    @http.route()
    def shop_payment_transaction(self, order_id, access_token, **kwargs):
        try:
            order_sudo = self._document_check_access(
                "sale.order", order_id, access_token
            )
        except MissingError:
            raise
        except AccessError:
            raise ValidationError(_("The access token is invalid.")) from None
        if order_sudo.website_cart_locked:
            raise ValidationError(order_sudo._get_website_cart_lock_message())
        return super().shop_payment_transaction(order_id, access_token, **kwargs)
