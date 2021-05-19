# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestAccountInvoiceValidateSendEmail(TransactionCase):
    def setUp(self):
        super(TestAccountInvoiceValidateSendEmail, self).setUp()
        self.account_rev = self.env["account.account"].create(
            {
                "code": "X2020",
                "name": "Sales Test",
                "user_type_id": self.ref("account.data_account_type_revenue"),
            }
        )
        self.journal = self.env["account.journal"].create(
            {"name": "Sale Journal - Test", "code": "STSJ", "type": "sale"}
        )
        receivable_id = self.env["account.account"].create(
            {
                "code": "X4040",
                "name": "Debtors Test",
                "user_type_id": self.ref("account.data_account_type_receivable"),
                "reconcile": True,
            }
        )
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test01@gmail.com",
                "property_account_receivable_id": receivable_id,
            }
        )
        self.workflow = self.env["sale.workflow.process"].create(
            {"name": "Send Invoice Test", "send_invoice": True}
        )

    def test_01_validate_invoice_no_send(self):
        invoice = self.env["account.invoice"].create(
            {
                "origin": "Test Invoice",
                "type": "out_invoice",
                "partner_id": self.partner.id,
                "journal_id": self.journal.id,
            }
        )
        self.env["account.invoice.line"].create(
            {
                "name": "Test 01",
                "account_id": self.account_rev.id,
                "price_unit": 100,
                "quantity": 1,
                "invoice_id": invoice.id,
            }
        )
        self.assertEqual(invoice.invoice_sent, False)
        invoice.sudo().action_invoice_open()
        # No invoice email should be sent at this point with no workflow
        # assignment.
        self.assertEqual(invoice.invoice_sent, False)

    def test_02_validate_invoice_send(self):
        # Remove report template from the email template to lighten the test load.
        template = self.env.ref(
            "account_invoice_validate_send_email.email_template_customer_invoice_validated"
        )
        template.report_template = False
        invoice = self.env["account.invoice"].create(
            {
                "origin": "Test Invoice",
                "type": "out_invoice",
                "account_id": self.partner.property_account_receivable_id.id,
                "partner_id": self.partner.id,
                "journal_id": self.journal.id,
            }
        )
        self.env["account.invoice.line"].create(
            {
                "name": "Test 01",
                "account_id": self.account_rev.id,
                "price_unit": 100,
                "quantity": 1,
                "invoice_id": invoice.id,
            }
        )
        self.assertEqual(invoice.invoice_sent, False)
        invoice.workflow_process_id = self.workflow
        invoice.sudo().action_invoice_open()
        # With workflow with send_invoice true, invoice email should be sent.
        self.assertEqual(invoice.invoice_sent, True)
