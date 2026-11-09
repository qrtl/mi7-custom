# Copyright 2026 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo.tests import HttpCase, tagged
from odoo.tests.common import TransactionCase, new_test_user


class AccountDeactivateCommon:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = new_test_user(
            cls.env, login="deactivate_b2c", groups="base.group_portal"
        )
        cls.partner = cls.user.partner_id
        cls.partner.write(
            {
                "name": "Taro Yamada",
                "user_type": "b2c",
                "email": "taro@example.com",
                "street": "1-2-3 Test",
            }
        )
        cls.delivery = cls.env["res.partner"].create(
            {
                "name": "Taro Yamada (Home)",
                "parent_id": cls.partner.id,
                "type": "delivery",
                "street": "4-5-6 Test",
            }
        )


class TestAccountDeactivate(AccountDeactivateCommon, TransactionCase):
    def _assert_anonymized(self, partners):
        self.assertRecordValues(
            partners,
            [
                {
                    "name": "退会済み %s" % partner.id,
                    "email": False,
                    "street": False,
                    "active": False,
                }
                for partner in partners
            ],
        )

    def test_deactivate(self):
        # Archived addresses and addresses under an address are reached too.
        archived = self.env["res.partner"].create(
            {
                "name": "Taro Yamada (Old)",
                "parent_id": self.partner.id,
                "type": "delivery",
                "street": "7-8-9 Test",
                "active": False,
            }
        )
        nested = self.env["res.partner"].create(
            {
                "name": "Taro Yamada (Office)",
                "parent_id": self.delivery.id,
                "type": "other",
                "street": "1-1-1 Test",
            }
        )
        other = self.env["res.partner"].create({"name": "Other Partner"})
        for partner in self.partner | other:
            partner.message_post(body="Chatter", attachments=[("doc.txt", b"data")])
        acquirer = self.env["payment.acquirer"].create(
            {"name": "Test Acquirer", "provider": "none", "state": "test"}
        )
        tx = self.env["payment.transaction"].create(
            {
                "acquirer_id": acquirer.id,
                "reference": "TEST-DEACTIVATE",
                "amount": 1100.0,
                "currency_id": self.env.company.currency_id.id,
                "partner_id": self.partner.id,
            }
        )
        self.assertEqual(tx.partner_email, "taro@example.com")
        self.user._deactivate_portal_account()
        self.assertFalse(self.user.exists())
        self._assert_anonymized(self.partner | self.delivery | archived | nested)
        self.assertFalse(tx.partner_email)
        partners = self.partner | other
        for model, model_field in (
            ("mail.message", "model"),
            ("ir.attachment", "res_model"),
        ):
            records = self.env[model].search(
                [(model_field, "=", "res.partner"), ("res_id", "in", partners.ids)]
            )
            self.assertEqual(set(records.mapped("res_id")), set(other.ids), model)

    def test_contact_under_company(self):
        company = self.env["res.partner"].create(
            {"name": "Test Company", "is_company": True, "email": "info@example.com"}
        )
        colleague = self.env["res.partner"].create(
            {
                "name": "Hanako Suzuki",
                "parent_id": company.id,
                "email": "hanako@example.com",
            }
        )
        self.partner.parent_id = company
        self.user._deactivate_portal_account()
        self._assert_anonymized(self.partner | self.delivery)
        self.assertRecordValues(
            company | colleague,
            [
                {"name": "Test Company", "email": "info@example.com", "active": True},
                {
                    "name": "Hanako Suzuki",
                    "email": "hanako@example.com",
                    "active": True,
                },
            ],
        )

    def test_cannot_deactivate(self):
        self.assertTrue(self.user._can_deactivate_portal_account())
        with self.subTest("B2B"):
            self.partner.user_type = "b2b"
            self.assertFalse(self.user._can_deactivate_portal_account())
            self.partner.user_type = "b2c"
        with self.subTest("archived contact under an address"):
            contact = self.env["res.partner"].create(
                {
                    "name": "Hanako Yamada",
                    "parent_id": self.delivery.id,
                    "active": False,
                }
            )
            self.assertFalse(self.user._can_deactivate_portal_account())
            contact.unlink()
        with self.subTest("another user on an address"):
            user = new_test_user(
                self.env,
                login="deactivate_delivery",
                groups="base.group_portal",
                partner_id=self.delivery.id,
            )
            self.assertFalse(self.user._can_deactivate_portal_account())
            user.unlink()
        with self.subTest("address account"):
            self.delivery.user_type = "b2c"
            user = new_test_user(
                self.env,
                login="deactivate_home",
                groups="base.group_portal",
                partner_id=self.delivery.id,
            )
            self.assertFalse(user._can_deactivate_portal_account())


@tagged("post_install", "-at_install")
class TestAccountDeactivateHttp(AccountDeactivateCommon, HttpCase):
    def _post_deactivate(self):
        self.authenticate(self.user.login, self.user.login)
        page = self.url_open("/my/security").text
        csrf_token = re.search(r'name="csrf_token" value="([^"]+)"', page)
        self.url_open(
            "/my/deactivate",
            data={
                "csrf_token": csrf_token.group(1),
                "account_deactivate_confirm": "on",
            },
        )
        return page

    def test_deactivate_route(self):
        self._post_deactivate()
        self.assertFalse(self.user.exists())

    def test_deactivate_route_blocked(self):
        # The form is hidden, and the controller refuses a direct POST.
        self.partner.user_type = "b2b"
        page = self._post_deactivate()
        self.assertNotIn('action="/my/deactivate"', page)
        self.assertTrue(self.user.exists())
