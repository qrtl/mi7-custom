# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestAccountInvoiceValidateSendEmail(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoiceValidateSendEmail, cls).setUpClass()
        cls.env["account.journal"].create(
            {"name": "Sale Journal - Test", "code": "STSJ", "type": "sale"}
        )
        acc_revenue = cls.env["account.account"].create(
            {
                "code": "X2020",
                "name": "Sales Test",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        acc_receivable = cls.env["account.account"].create(
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
                "property_account_receivable_id": acc_receivable.id,
            }
        )
        cls.workflow = cls.env["sale.workflow.process"].create(
            {
                "name": "Send Invoice Test",
                "create_invoice": True,
                "validate_invoice": True,
            }
        )
        cls.payment_term = cls.env["account.payment.term"].create(
            {"name": "Immediate Payment"}
        )
        cls.product1 = cls.env["product.product"].create(
            {
                "name": "test product",
                "type": "consu",
                "invoice_policy": "delivery",
                "property_account_income_id": acc_revenue.id,
            }
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "payment_term_id": cls.payment_term.id,
                "workflow_process_id": cls.workflow.id,
                "picking_policy": "direct",
            }
        )
        cls.env["sale.order.line"].create(
            {
                "order_id": cls.order.id,
                "product_id": cls.product1.id,
                "price_unit": 10.0,
            }
        )
        # Remove report template from the email template to lighten the test load.
        template = cls.env.ref(
            "account_invoice_validate_send_email.email_template_customer_invoice_validated"
        )
        template.report_template = False
        company = cls.env.ref("base.main_company")
        company.invoice_mail_template_id = template.id

    def test_01_validate_invoice_workflow_no_send(self):
        # Workflow send_invoice is false
        self.order.action_confirm()
        picking = self.order.picking_ids
        picking.validate_picking()
        self.env["automatic.workflow.job"].run()
        invoice = self.order.invoice_ids
        self.assertEqual(invoice.invoice_sent, False)

    def test_02_validate_invoice_workflow_send(self):
        # Workflow send_invoice is true
        self.workflow.send_invoice = True
        self.order.action_confirm()
        picking = self.order.picking_ids
        picking.validate_picking()
        self.env["automatic.workflow.job"].run()
        invoice = self.order.invoice_ids
        self.assertEqual(invoice.invoice_sent, True)

    def test_03_validate_invoice_payment_term_no_send(self):
        # Workflow send_invoice is true, payment term not_send_invoice is true
        self.workflow.send_invoice = True
        self.payment_term.not_send_invoice = True
        self.order.action_confirm()
        picking = self.order.picking_ids
        picking.validate_picking()
        self.env["automatic.workflow.job"].run()
        invoice = self.order.invoice_ids
        self.assertEqual(invoice.invoice_sent, False)

    def test_04_validate_invoice_picking_no_send(self):
        # Workflow send_invoice is true, picking not_send_invoice is true
        self.workflow.send_invoice = True
        self.order.action_confirm()
        picking = self.order.picking_ids
        picking.not_send_invoice = True
        picking.validate_picking()
        self.env["automatic.workflow.job"].run()
        invoice = self.order.invoice_ids
        self.assertEqual(invoice.picking_ids, picking)
        self.assertEqual(invoice.invoice_sent, False)

    def test_05_validate_invoices_send_invoice_picking(self):
        # Workflow send_invoice is true, picking not_send_invoice is false
        self.workflow.send_invoice = True
        # No automatic processing of invoice validation
        self.workflow.validate_invoice = False
        self.order.action_confirm()
        picking = self.order.picking_ids
        picking.validate_picking()
        self.env["automatic.workflow.job"].run()
        invoice = self.order.invoice_ids
        self.assertEqual(invoice.picking_ids.ids, picking.ids)
        invoice.action_post()
        self.assertEqual(invoice.invoice_sent, True)

    def test_06_validate_invoice_not_send_invoice_picking(self):
        self.workflow.send_invoice = True
        # No automatic processing of invoice validation
        self.workflow.validate_invoice = False
        self.order.action_confirm()
        picking = self.order.picking_ids
        picking.not_send_invoice = True
        picking.validate_picking()
        self.env["automatic.workflow.job"].run()
        invoice = self.order.invoice_ids
        self.assertEqual(invoice.picking_ids.ids, picking.ids)
        invoice.action_post()
        self.assertEqual(invoice.invoice_sent, False)

    def test_07_validate_invoice_no_picking_link(self):
        # Workflow send_invoice is true, picking not_send_invoice is true
        self.workflow.send_invoice = True
        # No automatic processing of invoice validation
        self.workflow.validate_invoice = False
        self.order.action_confirm()
        picking = self.order.picking_ids
        picking.not_send_invoice = True
        picking.validate_picking()
        self.env["automatic.workflow.job"].run()
        invoice = self.order.invoice_ids
        # Remove the direct link to the picking
        invoice.picking_ids = False
        self.assertEqual(invoice.picking_ids, self.env["stock.picking"].browse())
        invoice.action_post()
        self.assertEqual(invoice.invoice_sent, False)
