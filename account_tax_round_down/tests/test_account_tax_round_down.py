# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestAccountTaxRoundDown(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountTaxRoundDown, cls).setUpClass()
        cls.tax = cls.env["account.tax"].create(
            {
                "name": "Tax 10",
                "type_tax_use": "sale",
                "amount": 10,
            }
        )
        cls.company_jpy = cls.env["res.company"].create(
            {
                "name": "Japan company",
                "currency_id": cls.env.ref("base.JPY").id,
                "country_id": cls.env.ref("base.jp").id,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {"code": "test", "name": "test", "type": "sale"}
        )
        cls.partner = cls.env.ref("base.res_partner_3")
        cls.env.ref("account.data_account_type_receivable")
        cls.acc_revenue = cls.env["account.account"].create(
            {
                "code": "X2022",
                "name": "Tax Test",
                "user_type_id": cls.env.ref("account.data_account_type_revenue").id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test",
                "categ_id": cls.env.ref("product.product_category_all").id,
                "standard_price": 50,
                "list_price": 100,
                "type": "service",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "uom_po_id": cls.env.ref("uom.product_uom_unit").id,
                "description": "Test",
            }
        )

    def _create_invoice(self, journal_id, partner_id, invoice_line_data):
        invoice = self.env["account.move"].create(
            dict(
                name="Test Customer Invoice",
                journal_id=journal_id.id,
                partner_id=partner_id.id,
                invoice_line_ids=invoice_line_data,
                move_type="out_invoice",
                company_id=self.company_jpy.id,
            )
        )
        return invoice

    # Even if we don't install account_get_tax_totals_fix,
    # tax rounding is working when we add the tax first and then change price unit.
    # That why this test will not be failed.
    def test_account_tax_round_down_with_true(self):
        settings = self.env["res.config.settings"].create(
            {"tax_calculation_rounding_method": "round_globally"}
        )
        settings.execute()
        invoice_line_data = [
            (
                0,
                0,
                {
                    "product_id": self.product.id,
                    "quantity": 1,
                    "account_id": self.acc_revenue.id,
                    "name": "product test",
                    "price_unit": 23456,
                    "tax_ids": [(6, 0, self.tax.ids)],
                },
            )
        ]
        invoice = self._create_invoice(self.journal, self.partner, invoice_line_data)
        self.assertEqual(invoice.amount_tax, 2345)
        self.assertEqual(invoice.amount_total, 25801)

    def test_account_tax_round_down_with_false(self):
        self.company_jpy.write({"need_tax_round_down": False})
        invoice_line_data = [
            (
                0,
                0,
                {
                    "product_id": self.product.id,
                    "quantity": 1,
                    "account_id": self.acc_revenue.id,
                    "name": "product test",
                    "price_unit": 23456,
                    "tax_ids": [(6, 0, self.tax.ids)],
                },
            )
        ]

        invoice = self._create_invoice(self.journal, self.partner, invoice_line_data)
        self.assertEqual(invoice.amount_tax, 2346)
        self.assertEqual(invoice.amount_total, 25802)
