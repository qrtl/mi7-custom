# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleTaxRoundDown(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleTaxRoundDown, cls).setUpClass()
        cls.product = cls.env["product.product"].create({"name": "Test Product"})
        cls.partner = cls.env.ref("base.res_partner_1")
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

    def test_sale_tax_round_down_with_true(self):
        self.assertEqual(self.company_jpy.need_tax_round_down, True)
        settings = self.env["res.config.settings"].create(
            {"tax_calculation_rounding_method": "round_globally"}
        )
        settings.execute()
        so = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company_jpy.id,
            }
        )
        self.env["sale.order.line"].create(
            {
                "order_id": so.id,
                "product_id": self.product.id,
                "name": "Test",
                "product_uom_qty": 1,
                "price_unit": 23456,
                "tax_id": [(6, 0, self.tax.ids)],
            }
        )
        self.assertEqual(so.amount_tax, 2345)
        self.assertEqual(so.amount_total, 25801)

    def test_sale_tax_round_down_with_false(self):
        settings = self.env["res.config.settings"].create(
            {"need_tax_round_down": False}
        )
        settings.execute()
        so = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company_jpy.id,
            }
        )
        self.env["sale.order.line"].create(
            {
                "order_id": so.id,
                "product_id": self.product.id,
                "name": "Test",
                "product_uom_qty": 1,
                "price_unit": 23456,
                "tax_id": [(6, 0, self.tax.ids)],
            }
        )
        self.assertEqual(so.amount_tax, 2346)
        self.assertEqual(so.amount_total, 25802)
