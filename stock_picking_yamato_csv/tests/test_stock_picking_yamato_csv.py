# Copyright 2021 Quartile Limited

from odoo.exceptions import UserError
from odoo.tests.common import SavepointCase


class TestStockPickingYamatoCsv(SavepointCase):
    post_install = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        def _create_location(name, usage):
            return cls.env["stock.location"].create({"name": name, "usage": usage})

        cls.location = _create_location("location01", "inventory")
        cls.location_dest = _create_location("location02", "customer")
        cls.picking_type = cls.env.ref("stock.picking_type")
        cls.test_company = cls.env["res.company"].create({"name": "My Company"})
        cls.test_partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.uom = cls.env.ref("stock.product.uom")
        cls.picking = cls.env["stock.picking"].create(
            {
                "location_id": cls.location.id,
                "partner_id": cls.test_partner.id,
                "picking_type_id": cls.picking_type.id,
                "move_type": "Partial",
                "company_id": cls.test_company.id,
                "location_dest_id": cls.location_dest.id,
                "weight_uom_id": cls.uom.id,
                "yamato_carrier_code": "YTC01",
                "min_date": "1990-12-31 00:00:00",
            }
        )

    def test_01_prohibit_past_scheduled_date(self):
        self.picking.action_assign()
        with self.assertRaises(UserError):
            self.picking.generate_csv_report()
