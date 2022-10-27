# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields
from odoo.tests.common import TransactionCase


class TestPurchaseTaxRoundDown(TransactionCase):
    @classmethod
    def create_company(cls, values):
        return cls.env["res.company"].create(values)

    @classmethod
    def setUpClass(cls):
        super(TestPurchaseTaxRoundDown, cls).setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Test Product", "purchase_method": "purchase"}
        )
        cls.partner = cls.env.ref("base.res_partner_1")
        cls.tax = cls.env["account.tax"].create(
            {
                "name": "Tax 10",
                "type_tax_use": "purchase",
                "amount": 10,
            }
        )
        cls.company_jpy = cls.create_company(
            {
                "name": "Japan company",
                "currency_id": cls.env.ref("base.JPY").id,
                "country_id": cls.env.ref("base.jp").id,
            }
        )

    def test_purchase_tax_round_down_with_true(self):
        settings = self.env["res.config.settings"].create(
            {"tax_calculation_rounding_method": "round_globally"}
        )
        settings.execute()
        po = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company_jpy.id,
            }
        )
        self.env["purchase.order.line"].create(
            {
                "order_id": po.id,
                "product_id": self.product.id,
                "date_planned": fields.Datetime.now(),
                "name": "Test",
                "product_qty": 1,
                "price_unit": 23456,
                "taxes_id": [(6, 0, self.tax.ids)],
            }
        )
        self.assertEqual(po.amount_tax, 2345)
        self.assertEqual(po.amount_total, 25801)

    def test_purchase_tax_round_down_with_false(self):
        settings = self.env["res.config.settings"].create(
            {"need_tax_round_down": False}
        )
        settings.execute()
        po = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company_jpy.id,
            }
        )
        self.env["purchase.order.line"].create(
            {
                "order_id": po.id,
                "product_id": self.product.id,
                "date_planned": fields.Datetime.now(),
                "name": "Test",
                "product_qty": 1,
                "price_unit": 23456,
                "taxes_id": [(6, 0, self.tax.ids)],
            }
        )
        self.assertEqual(po.amount_tax, 2346)
        self.assertEqual(po.amount_total, 25802)
