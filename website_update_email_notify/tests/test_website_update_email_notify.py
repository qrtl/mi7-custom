# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestWebsiteUpdateEmailNotify(TransactionCase):
    post_install = True

    def setUp(self):
        super(TestWebsiteUpdateEmailNotify, self).setUp()
        self.user = self.env["res.users"].create(
            {"name": "Test Partner", "login": "test01@gmail.com"}
        )

    def test_01_update_login_email(self):
        self.user._update_login_email("test01@gmail.com", "test0.1@gmail.com")
        self.assertEqual(self.user.login, "test0.1@gmail.com")
