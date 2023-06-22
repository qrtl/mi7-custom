from odoo.tests.common import TransactionCase


class TestSaleUserType(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Product1", "type": "product"}
        )
        cls.commercial_partner_id = cls.env["res.partner"].create(
            {
                "name": "Commercial Partner",
                "company_type": "company",
                "user_type": "b2c",
            }
        )
        cls.partner_id = cls.env["res.partner"].create(
            {
                "name": "Partner",
                "parent_id": cls.commercial_partner_id.id,
            }
        )

    def create_sale_order(self):
        so = self.env["sale.order"].create(
            {
                "partner_id": self.partner_id.id,
                "partner_invoice_id": self.partner_id.id,
                "partner_shipping_id": self.partner_id.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "product_uom_qty": 2,
                            "product_uom": self.product.uom_id.id,
                            "price_unit": 300,
                        },
                    ),
                ],
            }
        )
        so.action_confirm()
        return so

    def test_01_sale_user_type(self):
        order = self.create_sale_order()
        self.assertEqual(order.user_type, self.commercial_partner_id.user_type)
        sale_b2c_sequence = self.env["ir.sequence"].search(
            [("code", "=", "sale.b2c.sequence")]
        )
        self.assertEqual(order.name[0:7], sale_b2c_sequence.prefix)
        picking_b2c_sequence = self.env["ir.sequence"].search(
            [("code", "=", "picking.b2c.sequence")]
        )
        self.assertEqual(order.picking_ids[0].name[0:7], picking_b2c_sequence.prefix)
