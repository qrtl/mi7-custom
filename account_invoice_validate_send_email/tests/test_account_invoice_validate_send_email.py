# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestAccountInvoiceValidateSendEmail(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoiceValidateSendEmail, cls).setUpClass()
        account_rev = cls.env["account.account"].create(
            {
                "code": "X2020",
                "name": "Sales Test",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        journal = cls.env["account.journal"].create(
            {"name": "Sale Journal - Test", "code": "STSJ", "type": "sale"}
        )
        receivable_id = cls.env["account.account"].create(
            {
                "code": "X4040",
                "name": "Debtors Test",
                "user_type_id": cls.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test01@gmail.com",
                "property_account_receivable_id": receivable_id,
            }
        )
        cls.workflow = cls.env["sale.workflow.process"].create(
            {"name": "Send Invoice Test", "send_invoice": True}
        )
        cls.payment_term = cls.env["account.payment.term"].create(
            {
                "name": "Immediate Payment",
                # "not_send_invoice": True,
            }
        )
        location = cls.env["stock.location"].search(
            [("usage", "=", "production")], limit=1
        )
        picking_type = cls.env["stock.picking.type"].search(
            [("code", "=", "outgoing")], limit=1
        )
        picking = cls.env["stock.picking"].create(
            {
                "partner_id": partner.id,
                "location_id": location.id,
                "picking_type_id": picking_type.id,
                "location_dest_id": location.id,
            }
        )

        cls.invoice = cls.env["account.invoice"].create(
            {
                "origin": "Test Invoice",
                "type": "out_invoice",
                "partner_id": partner.id,
                "journal_id": journal.id,
            }
        )
        cls.env["account.invoice.line"].create(
            {
                "name": "Test 01",
                "account_id": account_rev.id,
                "price_unit": 100,
                "quantity": 1,
                "invoice_id": cls.invoice.id,
            }
        )
        # Remove report template from the email template to lighten the test load.
        template = cls.env.ref(
            "account_invoice_validate_send_email.email_template_customer_invoice_validated"
        )
        template.report_template = False
        cls.invoice.company_id.invoice_mail_template_id = template.id
        cls.invoice.picking_ids = [picking.id]

    def test_01_validate_invoice_no_workflow(self):
        # Without workflow
        self.assertEqual(self.invoice.invoice_sent, False)
        self.invoice.sudo().action_invoice_open()
        self.assertEqual(self.invoice.invoice_sent, False)

    def test_02_validate_invoice_workflow_no_term(self):
        # With workflow, without payment term
        self.assertEqual(self.invoice.invoice_sent, False)
        self.invoice.workflow_process_id = self.workflow
        self.invoice.sudo().action_invoice_open()
        self.assertEqual(self.invoice.invoice_sent, True)

    def test_03_validate_invoice_workflow_term_not_send(self):
        # With workflow, with payment term (no_send_invoice is true)
        self.assertEqual(self.invoice.invoice_sent, False)
        self.invoice.workflow_process_id = self.workflow
        self.payment_term.not_send_invoice = True
        self.invoice.payment_term_id = self.payment_term
        self.invoice.sudo().action_invoice_open()
        self.assertEqual(self.invoice.invoice_sent, False)

    def test_04_validate_invoice_workflow_term_send(self):
        # With workflow, with payment term (no_send_invoice is false)
        self.assertEqual(self.invoice.invoice_sent, False)
        self.invoice.workflow_process_id = self.workflow
        self.invoice.payment_term_id = self.payment_term
        self.invoice.sudo().action_invoice_open()
        self.assertEqual(self.invoice.invoice_sent, True)
