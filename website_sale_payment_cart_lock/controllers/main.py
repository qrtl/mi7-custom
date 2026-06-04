# Copyright 2026 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, fields, http, tools
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request

from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
from odoo.addons.website_sale.controllers.main import PaymentPortal as WebsiteSalePaymentPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale as WebsiteSaleController


class WebsiteSale(WebsiteSaleController):
    def _get_cart_lock_message(self, order):
        return order._get_website_cart_lock_message()

    def _is_cart_locked(self, order):
        return bool(order and order._is_website_cart_locked())

    def _get_locked_cart_response(self, order, line_id=None):
        message = self._get_cart_lock_message(order)
        quantity = 0
        if line_id:
            order_line = order.order_line.filtered(lambda line: line.id == int(line_id))[:1]
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
            "website_sale.short_cart_summary": request.env["ir.ui.view"]._render_template(
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
            response.qcontext["cart_locked_message"] = self._get_cart_lock_message(order)
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
    @http.route("/shop/payment/transaction/<int:order_id>", type="json", auth="public", website=True)
    def shop_payment_transaction(self, order_id, access_token, **kwargs):
        try:
            order_sudo = self._document_check_access("sale.order", order_id, access_token)
        except MissingError as error:
            raise error
        except AccessError:
            raise ValidationError(_("The access token is invalid."))

        if order_sudo._is_website_cart_locked():
            raise ValidationError(order_sudo._get_website_cart_lock_message())

        if order_sudo.state == "cancel":
            raise ValidationError(_("The order has been canceled."))

        if tools.float_compare(
            kwargs["amount"],
            order_sudo.amount_total,
            precision_rounding=order_sudo.currency_id.rounding,
        ):
            raise ValidationError(_("The cart has been updated. Please refresh the page."))

        kwargs.update(
            {
                "reference_prefix": None,
                "sale_order_id": order_id,
            }
        )
        kwargs.pop("custom_create_values", None)

        order_sudo.action_lock_website_cart()
        try:
            tx_sudo = self._create_transaction(
                custom_create_values={"sale_order_ids": [Command.set([order_id])]},
                **kwargs,
            )

            last_tx_id = request.session.get("__website_sale_last_tx_id")
            last_tx = request.env["payment.transaction"].browse(last_tx_id).sudo().exists()
            if last_tx:
                PaymentPostProcessing.remove_transactions(last_tx)
            request.session["__website_sale_last_tx_id"] = tx_sudo.id

            return tx_sudo._get_processing_values()
        except Exception:
            order_sudo.action_unlock_website_cart()
            raise
