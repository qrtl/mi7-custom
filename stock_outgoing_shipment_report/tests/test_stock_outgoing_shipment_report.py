# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests import SavepointCase, tagged


# @tagged("post_install", "-at_install")
# class TestAccountPaymentImportSbt(SavepointCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.partner = cls.env["res.partner"].create(
#             {
#                 "name": "Test Partner",
#                 "state_id": cls.env.ref("base.state_jp_jp-02").id,
#                 "city": "City",
#                 "street": "Street",
#                 "street2": "Street2",
#                 "delivery_time": "test",
#             }
#         )
#         cls.env.ref("delivery.free_delivery_carrier").write({"shipping_mode": "10"})
#         cls.product = cls.env["product.product"].create(
#             {"name": "Product A", "default_code": "Test Code"}
#         )
#         cls.sale_order = cls.env["sale.order"].create(
#             {
#                 "partner_id": cls.partner.id,
#                 "carrier_id": cls.env.ref("delivery.free_delivery_carrier").id,
#             }
#         )
#         cls.order_line = cls.env["sale.order.line"].create(
#             {
#                 "order_id": cls.sale_order.id,
#                 "product_id": cls.product.id,
#                 "product_uom_qty": 1.0,
#                 "price_unit": 100.0,
#                 "client_order_ref": "ref0001",
#             }
#         )
#         cls.order_line = cls.env["sale.order.line"].create(
#             {
#                 "order_id": cls.sale_order.id,
#                 "product_id": cls.product.id,
#                 "product_uom_qty": 1.0,
#                 "price_unit": 100.0,
#                 "client_order_ref": "ref0002",
#             }
#         )
#         cls.sale_order.action_confirm()
#         cls.pickings = cls.sale_order.picking_ids
#         cls.pickings.mapped("move_lines").update({"note": "Test Note"})

#     def test_01_get_shipping_address(self):
#         self.assertEqual(
#             self.partner._get_shipping_address(), "AomoriCityStreetStreet2"
#         )

#     def test_02_generate_stock_outgoing_shipment_report(self):
#         self.pickings.generate_stock_outgoing_shipment_report()
#         report_lines = self.env["stock.outgoing.shipment.report"].search([])
#         self.assertEqual(len(report_lines), 2)
#         test_line = report_lines[0]

#         self.assertEqual(test_line.shipping_mode, "10")
#         self.assertEqual(
#             test_line.carrier_name,
#             self.env.ref("delivery.free_delivery_carrier").name[:20],
#         )
#         self.assertEqual(test_line.product_code, self.product.default_code[:7])
#         self.assertEqual(test_line.product_name, self.product.name)
#         self.assertEqual(test_line.client_order_ref, "ref0001")
#         self.assertEqual(test_line.memo, "Test Note")
