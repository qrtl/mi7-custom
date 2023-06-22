from odoo.tests.common import TransactionCase


class TestPartnerBirthMonth(TransactionCase):
    def setUp(self):
        super(TestPartnerBirthMonth, self).setUp()
        self.partner_admin = self.env.ref("base.partner_admin")
        self.partner_admin.write({"birthday": "1991-09-05"})

    def test_compute_birth_month(self):
        self.assertEqual(self.partner_admin.birth_month, 9)
        partner = self.env["res.partner"].create(
            {"name": "Test Partner", "birthday": "2000-03-05"}
        )
        self.assertEqual(partner.birth_month, 3)
