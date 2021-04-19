# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError
from odoo.tests import SavepointCase


class TestStockPickingExportReport(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestStockPickingExportReport, cls).setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "state_id": cls.env.ref("base.state_jp_jp-02").id,
                "city": "City",
                "street": "Street",
                "street2": "Street2",
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Product A", "default_code": "Test Code"}
        )
        cls.sale_order = cls.env["sale.order"].create({"partner_id": cls.partner.id})
        cls.order_line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.product.id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
            }
        )
        cls.order_line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.product.id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
            }
        )
        cls.sale_order.action_confirm()
        cls.pickings = cls.sale_order.picking_ids
        cls.pickings.mapped("move_lines").update({"note": "Test Note"})

    def test_01_generate_stock_outgoing_shipment_report(self):
        self.pickings.generate_stock_outgoing_shipment_report()
        report_lines = self.env["stock.outgoing.shipment.report"].search([])
        self.assertEqual(len(report_lines), 2)
        self.assertTrue(all(self.pickings.mapped("is_exported")))
        with self.assertRaises(UserError):
            self.pickings.generate_stock_outgoing_shipment_report()
