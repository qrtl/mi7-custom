# Copyright 2026 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command
from odoo.tests.common import tagged

from odoo.addons.payment.tests.common import PaymentCommon
from odoo.addons.website.tools import MockRequest
from odoo.addons.website_sale_payment_cart_lock.controllers.main import (
    PaymentPortal,
    WebsiteSale,
)


@tagged("post_install", "-at_install")
class TestWebsiteSalePaymentCartLock(PaymentCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].browse(1)
        cls.public_user = cls.env.ref("base.public_user")
        cls.cart_controller = WebsiteSale()
        cls.payment_controller = PaymentPortal()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Website Cart Lock Product",
                "sale_ok": True,
                "website_published": True,
                "lst_price": 100.0,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].search(
            [("currency_id", "=", cls.currency.id)], limit=1
        )
        if not cls.pricelist:
            cls.pricelist = cls.env["product.pricelist"].create(
                {
                    "name": "Website Cart Lock Test Pricelist",
                    "currency_id": cls.currency.id,
                }
            )

    def _create_backend_order(self):
        return self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "pricelist_id": self.pricelist.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 100.0,
                        }
                    )
                ],
            }
        )

    def _create_website_order(self):
        website = self.website.with_user(self.public_user)
        product = self.product.with_user(self.public_user)
        with MockRequest(product.env, website=website):
            self.cart_controller.cart_update_json(product_id=product.id, add_qty=1)
            order = website.sale_get_order()
            order._portal_ensure_token()
        return order.sudo()

    def test_cart_update_is_blocked_when_order_is_locked(self):
        order = self._create_backend_order()
        order.action_lock_website_cart()

        with self.assertRaises(UserError):
            order._cart_update(
                product_id=self.product.id,
                line_id=order.order_line.id,
                set_qty=0,
            )

    def test_cart_update_json_returns_warning_for_locked_cart(self):
        order = self._create_website_order()
        order.action_lock_website_cart()
        initial_qty = order.order_line.product_uom_qty

        website = self.website.with_user(self.public_user)
        product = self.product.with_user(self.public_user)
        with MockRequest(product.env, website=website, sale_order_id=order.id):
            values = self.cart_controller.cart_update_json(
                product_id=product.id,
                line_id=order.order_line.id,
                set_qty=0,
            )

        order.invalidate_cache()
        self.assertEqual(values["warning"], order._get_website_cart_lock_message())
        self.assertEqual(values["quantity"], initial_qty)
        self.assertEqual(order.order_line.product_uom_qty, initial_qty)

    def test_done_transaction_unlocks_cart(self):
        order = self._create_backend_order()
        order.action_lock_website_cart()
        tx = self.create_transaction(
            "redirect",
            amount=order.amount_total,
            currency_id=order.currency_id.id,
            partner_id=order.partner_id.id,
            sale_order_ids=[Command.set([order.id])],
        )

        tx._set_done()
        order.invalidate_cache()

        self.assertFalse(order.website_cart_locked)
        self.assertFalse(order.website_cart_lock_date)

    def test_error_transaction_unlocks_cart(self):
        order = self._create_backend_order()
        order.action_lock_website_cart()
        tx = self.create_transaction(
            "redirect",
            amount=order.amount_total,
            currency_id=order.currency_id.id,
            partner_id=order.partner_id.id,
            sale_order_ids=[Command.set([order.id])],
        )

        tx._set_error("test error")
        order.invalidate_cache()

        self.assertFalse(order.website_cart_locked)
        self.assertFalse(order.website_cart_lock_date)

    def test_shop_payment_transaction_locks_order(self):
        order = self._create_website_order()
        website = self.website.with_user(self.public_user)
        product = self.product.with_user(self.public_user)

        with MockRequest(product.env, website=website, sale_order_id=order.id):
            processing_values = self.payment_controller.shop_payment_transaction(
                order.id,
                order.access_token,
                amount=order.amount_total,
                currency_id=order.currency_id.id,
                partner_id=order.partner_id.id,
                payment_option_id=self.acquirer.id,
                flow="redirect",
                tokenization_requested=False,
                landing_route="/shop/payment/validate",
            )

        order.invalidate_cache()
        self.assertTrue(order.website_cart_locked)
        self.assertTrue(order.transaction_ids)
        self.assertEqual(
            processing_values["reference"], order.transaction_ids[:1].reference
        )

    def test_shop_payment_transaction_rejects_locked_order(self):
        order = self._create_website_order()
        order.action_lock_website_cart()
        website = self.website.with_user(self.public_user)
        product = self.product.with_user(self.public_user)

        with MockRequest(product.env, website=website, sale_order_id=order.id):
            with self.assertRaises(ValidationError):
                self.payment_controller.shop_payment_transaction(
                    order.id,
                    order.access_token,
                    amount=order.amount_total,
                    currency_id=order.currency_id.id,
                    partner_id=order.partner_id.id,
                    payment_option_id=self.acquirer.id,
                    flow="redirect",
                    tokenization_requested=False,
                    landing_route="/shop/payment/validate",
                )
