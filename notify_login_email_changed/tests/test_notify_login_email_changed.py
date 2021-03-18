# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestNotifyLoginEmailChanged(TransactionCase):
    def setUp(self):
        super(TestNotifyLoginEmailChanged, self).setUp()
        self.user = self.env["res.users"].create(
            {"name": "Test Partner", "login": "test01@gmail.com"}
        )

    def test_01_send_email(self):
        partner = self.user.partner_id
        self.assertEqual(
            partner._send_email(
                old_email="test01@gmail.com", new_email="test0.1@gmail.com"
            ),
            True,
        )

    def test_02_update_login_email(self):
        partner = self.user.partner_id
        users = partner._update_login_email(new_email="test0.1@gmail.com")
        self.assertEqual(users[0].login, "test0.1@gmail.com")
