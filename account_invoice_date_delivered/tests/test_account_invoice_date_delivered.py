from odoo.tests.common import TransactionCase

class TestAccountInvoiceDateDelivered(TransactionCase):
    def update_product_qty(self, product):

        product_qty = self.env["stock.change.product.qty"].create(
            {
                "product_id": product.id,
                "product_tmpl_id": product.product_tmpl_id.id,
                "new_quantity": 100.0,
            }
        )
        product_qty.change_product_qty()
        return product_qty

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
                {"name": "Product1", "type": "product"}
            )
        cls.partner_id = cls.env['res.partner'].create({
                'name': 'Partner',
            })
        cls.so = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_id.id,
                "partner_invoice_id": cls.partner_id.id,
                "partner_shipping_id": cls.partner_id.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product.name,
                            "product_id": cls.product.id,
                            "product_uom_qty": 2,
                            "product_uom": cls.product.uom_id.id,
                            "price_unit": 300,
                        },
                    ),
                ],
            }
        )

    def test_01_account_invoice_date_delivered(self):
        self.update_product_qty(self.product)
        self.so.action_confirm()
        pick = self.so.picking_ids
        pick.move_line_ids.write({"qty_done": 2})
        pick._action_done()
        inv = self.so._create_invoices()
        self.assertEqual(pick.date_done, inv.time_delivered)
    