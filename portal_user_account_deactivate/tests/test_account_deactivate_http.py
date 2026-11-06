# Copyright 2026 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo.tests import HttpCase, tagged

from .common import AccountDeactivateCommon


@tagged("post_install", "-at_install")
class TestAccountDeactivateHttp(AccountDeactivateCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_account_deactivate_data()

    def _post_deactivate(self):
        login = self.user.login
        self.authenticate(login, login)
        response = self.url_open("/my/security")
        self.assertEqual(response.status_code, 200)
        csrf_token = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
        return response, self.url_open(
            "/my/deactivate",
            data={
                "csrf_token": csrf_token.group(1),
                "account_deactivate_confirm": "on",
            },
        )

    def test_deactivate_route(self):
        login = self.user.login
        __, response = self._post_deactivate()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            self.env["res.users"]
            .with_context(active_test=False)
            .search([("login", "=", login)])
        )
        self.assertEqual(self.partner.name, "退会済み %s" % self.partner.id)
        self.assertFalse(self.partner.email)
        self.assertFalse(self.partner.active)
        self.assertFalse(self.delivery.active)

    def test_deactivate_route_blocked(self):
        self.partner.user_type = "b2b"
        security_page, __ = self._post_deactivate()
        self.assertIn("please contact us", security_page.text)
        self.assertNotIn('action="/my/deactivate"', security_page.text)
        self.assertTrue(self.user.active)
        self.assertEqual(self.partner.name, "Taro Yamada")
