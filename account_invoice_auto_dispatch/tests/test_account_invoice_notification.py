# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestAccountInvoiceNotification(TransactionCase):
    def setUp(self):
        super(TestAccountInvoiceNotification, self).setUp()

    def test_send_notify(self):
        IrModelData = self.env["ir.model.data"]
        partner_obj = self.env["res.partner"]
        journal_obj = self.env["account.journal"]
        account_obj = self.env["account.account"]

        self.journal = journal_obj.create(
            {"name": "Sale Journal - Test", "code": "STSJ", "type": "sale"}
        )

        self.partner = partner_obj.create(
            {"name": "Test Partner", "email": "test01@gmail.com"}
        )
        self.invoice = self.env["account.invoice"].create(
            {
                "origin": "Test Invoice",
                "type": "out_invoice",
                "account_id": self.partner.property_account_receivable_id.id,
                "partner_id": self.partner.id,
                "journal_id": self.journal.id,
            }
        )

        user_type_id = IrModelData.xmlid_to_res_id("account.data_account_type_revenue")
        uom_id = IrModelData.xmlid_to_res_id("uom.product_uom_unit")
        account_rev = account_obj.create(
            {
                "code": "X2020",
                "name": "Sales - Test Sales Account",
                "user_type_id": user_type_id,
                "reconcile": True,
            }
        )
        self.env["account.invoice.line"].create(
            {
                "name": "Test 01",
                "account_id": account_rev.id,
                "price_unit": 100,
                "quantity": 1,
                "uom_id": uom_id,
                "product_id": False,
                "invoice_id": self.invoice.id,
            }
        )
        self.invoice.sudo().action_invoice_open()
        self.assertEqual(self.invoice.invoice_sent, True)
        self.assertEqual(self.invoice.state, "open")
        self.invoice.sudo().action_cancel()
        self.invoice.sudo().action_invoice_draft()
        self.assertEqual(self.invoice.invoice_sent, False)
        self.assertEqual(self.invoice.state, "draft")
