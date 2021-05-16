# Copyright 2020 Quartile Limited
import base64
import os

from odoo import fields
from odoo.tests import SavepointCase, tagged
from odoo.tools.misc import file_open


@tagged("post_install", "-at_install")
class TestAccountPaymentImportSbt(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.usd_bank = cls.env["account.journal"].create(
            {
                "name": "USD_BANK",
                "code": "USDBNK",
                "type": "bank",
                "currency_id": cls.env.ref("base.USD").id,
            }
        )
        cls.eur_bank = cls.env["account.journal"].create(
            {
                "name": "EUR_BANK",
                "code": "EURBNK",
                "type": "bank",
                "currency_id": cls.env.ref("base.EUR").id,
            }
        )
        cls.eur_pricelist = cls.env["product.pricelist"].create(
            {"name": "EUR Pricelist", "currency_id": cls.env.ref("base.EUR").id}
        )
        cls.test_product = cls.env["product.product"].create(
            {"name": "Test Product", "type": "service", "invoice_policy": "order"}
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner 01",
                "customer": True,
                "supplier": True,
                "ref": "Test Ref",
            }
        )
        # USD Orders (Company Currency)
        cls.usd_sale_order = cls.env["sale.order"].create(
            {
                "name": "TESTSO0001",
                "partner_id": cls.partner.id,
                "pricelist_id": cls.env.ref("product.list0").id,
            }
        )
        cls.env["sale.order.line"].create(
            {
                "order_id": cls.usd_sale_order.id,
                "product_id": cls.test_product.id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
                "tax_id": False,
            }
        )
        cls.usd_purchase_order = cls.env["purchase.order"].create(
            {
                "name": "TESTPO0001",
                "partner_id": cls.partner.id,
                "currency_id": cls.env.ref("base.USD").id,
            }
        )
        cls.env["purchase.order.line"].create(
            {
                "order_id": cls.usd_purchase_order.id,
                "product_id": cls.test_product.id,
                "name": cls.test_product.name,
                "date_planned": fields.Datetime.now(),
                "product_qty": 1.0,
                "product_uom": cls.test_product.uom_po_id.id,
                "price_unit": 100.0,
            }
        )
        # EUR Orders
        cls.eur_sale_order = cls.env["sale.order"].create(
            {
                "name": "TESTSO0002",
                "partner_id": cls.partner.id,
                "pricelist_id": cls.eur_pricelist.id,
            }
        )
        cls.env["sale.order.line"].create(
            {
                "order_id": cls.eur_sale_order.id,
                "product_id": cls.test_product.id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
                "tax_id": False,
            }
        )
        cls.eur_purchase_order = cls.env["purchase.order"].create(
            {
                "name": "TESTPO0002",
                "partner_id": cls.partner.id,
                "currency_id": cls.env.ref("base.EUR").id,
            }
        )
        cls.env["purchase.order.line"].create(
            {
                "order_id": cls.eur_purchase_order.id,
                "product_id": cls.test_product.id,
                "name": cls.test_product.name,
                "date_planned": fields.Datetime.now(),
                "product_qty": 1.0,
                "product_uom": cls.test_product.uom_po_id.id,
                "price_unit": 100.0,
            }
        )
        # Confirm orders
        cls.usd_sale_order.action_confirm()
        cls.eur_sale_order.action_confirm()
        cls.usd_purchase_order.button_confirm()
        cls.eur_purchase_order.button_confirm()
        # Create Invoices
        cls.usd_sale_invoice = cls.env["account.invoice"].browse(
            cls.usd_sale_order.action_invoice_create()
        )
        cls.eur_sale_invoice = cls.env["account.invoice"].browse(
            cls.eur_sale_order.action_invoice_create()
        )
        cls.usd_purchase_invoice = cls.env["account.invoice"].create(
            {
                "partner_id": cls.partner.id,
                "purchase_id": cls.usd_purchase_order.id,
                "account_id": cls.partner.property_account_payable_id.id,
                "type": "in_invoice",
            }
        )
        cls.usd_purchase_invoice.purchase_order_change()
        for invoice_line in cls.usd_purchase_invoice.invoice_line_ids:
            invoice_line.write({"price_unit": 100.0})
            invoice_line.write({"quantity": 1.0})
        cls.usd_purchase_order.invoice_ids = [(6, 0, [cls.usd_purchase_invoice.id])]
        cls.eur_purchase_invoice = cls.env["account.invoice"].create(
            {
                "partner_id": cls.partner.id,
                "purchase_id": cls.eur_purchase_order.id,
                "account_id": cls.partner.property_account_payable_id.id,
                "type": "in_invoice",
            }
        )
        cls.eur_purchase_invoice.purchase_order_change()
        for invoice_line in cls.eur_purchase_invoice.invoice_line_ids:
            invoice_line.write({"price_unit": 100.0})
            invoice_line.write({"quantity": 1.0})
        cls.eur_purchase_order.invoice_ids = [(6, 0, [cls.eur_purchase_invoice.id])]
        # Validate Invoices
        cls.usd_sale_invoice.action_invoice_open()
        cls.eur_sale_invoice.action_invoice_open()
        cls.usd_purchase_invoice.action_invoice_open()
        cls.eur_purchase_invoice.action_invoice_open()

        refund = (
            cls.env["account.invoice.refund"]
            .with_context(
                {
                    "active_ids": [cls.usd_sale_invoice.id],
                    "active_id": cls.usd_sale_invoice,
                }
            )
            .create({"filter_refund": "refund", "description": "Refund Test"})
        )
        result = refund.invoice_refund()
        cls.usd_sale_refund_invoice = cls.env["account.invoice"].browse(
            result.get("domain")[1][2]
        )
        cls.usd_sale_refund_invoice.write({"origin": cls.usd_sale_invoice.number})
        cls.usd_sale_refund_invoice.action_invoice_open()
        refund = (
            cls.env["account.invoice.refund"]
            .with_context(
                {
                    "active_ids": [cls.eur_sale_invoice.id],
                    "active_id": cls.eur_sale_invoice,
                }
            )
            .create({"filter_refund": "refund", "description": "Refund Test"})
        )
        result = refund.invoice_refund()
        cls.eur_sale_refund_invoice = cls.env["account.invoice"].browse(
            result.get("domain")[1][2]
        )
        cls.eur_sale_refund_invoice.write({"origin": cls.eur_sale_invoice.number})
        cls.eur_sale_refund_invoice.action_invoice_open()

        refund = (
            cls.env["account.invoice.refund"]
            .with_context(
                {
                    "active_ids": [cls.usd_purchase_invoice.id],
                    "active_id": cls.usd_purchase_invoice,
                }
            )
            .create({"filter_refund": "refund", "description": "Refund Test"})
        )
        result = refund.invoice_refund()
        cls.usd_purchase_refund_invoice = cls.env["account.invoice"].browse(
            result.get("domain")[1][2]
        )
        cls.usd_purchase_refund_invoice.action_invoice_open()
        refund = (
            cls.env["account.invoice.refund"]
            .with_context(
                {
                    "active_ids": [cls.eur_purchase_invoice.id],
                    "active_id": cls.eur_purchase_invoice,
                }
            )
            .create(
                {
                    "filter_refund": "refund",
                    "description": "Refund Test",
                    "date": cls.eur_purchase_invoice.date_invoice,
                }
            )
        )
        result = refund.invoice_refund()
        cls.eur_purchase_refund_invoice = cls.env["account.invoice"].browse(
            result.get("domain")[1][2]
        )
        cls.eur_purchase_refund_invoice.action_invoice_open()

    # Import sale payment csv
    def test_01_import_sale_payment(self):
        file_path = os.path.join(
            "account_payment_import_sbt", "tests", "test_sale_import.csv"
        )
        sale_import_file = file_open(file_path, "rb")
        sale_import_file = sale_import_file.read()
        import_wizard = self.env["account.payment.import"].create(
            {
                "import_type": "sale",
                "import_file": base64.encodestring(sale_import_file),
                "file_name": file_path,
            }
        )
        res = import_wizard.confirm_import_payment()
        result_log = self.env["error.log"].browse(res["res_id"])
        self.assertEqual(result_log.state, "done")
        self.env["account.payment"].cron_validate_payment(1000)
        self.assertEqual(self.usd_sale_invoice.state, "paid")
        self.assertEqual(self.eur_sale_invoice.state, "paid")

    # Import sale refund csv
    def test_02_import_sale_refund(self):
        # Refund case
        file_path = os.path.join(
            "account_payment_import_sbt", "tests", "test_sale_refund_import.csv"
        )
        sale_import_file = file_open(file_path, "rb")
        sale_import_file = sale_import_file.read()
        import_wizard = self.env["account.payment.import"].create(
            {
                "import_type": "sale",
                "import_file": base64.encodestring(sale_import_file),
                "file_name": file_path,
            }
        )
        res = import_wizard.confirm_import_payment()
        result_log = self.env["error.log"].browse(res["res_id"])
        self.assertEqual(result_log.state, "done")
        self.env["account.payment"].cron_validate_payment(1000)
        self.assertEqual(self.usd_sale_refund_invoice.state, "paid")
        self.assertEqual(self.eur_sale_refund_invoice.state, "paid")

    # Import purchase payment csv (Shift-JIS)
    def test_03_import_purchase_payment(self):
        file_path = os.path.join(
            "account_payment_import_sbt", "tests", "test_purchase_import.csv"
        )
        purchase_import_file = file_open(file_path, "rb")
        purchase_import_file = purchase_import_file.read()
        import_wizard = self.env["account.payment.import"].create(
            {
                "import_type": "purchase",
                "import_file": base64.encodestring(purchase_import_file),
                "file_name": file_path,
            }
        )
        res = import_wizard.confirm_import_payment()
        result_log = self.env["error.log"].browse(res["res_id"])
        self.assertEqual(result_log.state, "done")
        self.env["account.payment"].cron_validate_payment(1000)
        self.assertEqual(self.usd_purchase_invoice.state, "paid")
        self.assertEqual(self.eur_purchase_invoice.state, "paid")

    # Import purchase refund csv (Shift-JIS)
    def test_04_import_purchase_refund(self):
        file_path = os.path.join(
            "account_payment_import_sbt", "tests", "test_purchase_refund_import.csv"
        )
        purchase_import_file = file_open(file_path, "rb")
        purchase_import_file = purchase_import_file.read()
        import_wizard = self.env["account.payment.import"].create(
            {
                "import_type": "purchase",
                "import_file": base64.encodestring(purchase_import_file),
                "file_name": file_path,
            }
        )
        res = import_wizard.confirm_import_payment()
        result_log = self.env["error.log"].browse(res["res_id"])
        self.assertEqual(result_log.state, "done")
        self.env["account.payment"].cron_validate_payment(1000)
        self.assertEqual(self.usd_purchase_refund_invoice.state, "paid")
        self.assertEqual(self.eur_purchase_refund_invoice.state, "paid")
