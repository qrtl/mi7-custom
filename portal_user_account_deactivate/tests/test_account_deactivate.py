# Copyright 2026 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase, new_test_user

from .common import AccountDeactivateCommon


# post_install, so that the link to sales orders is tested when sale is installed.
@tagged("post_install", "-at_install")
class TestAccountDeactivate(AccountDeactivateCommon, TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_account_deactivate_data()
        cls.other_partner = cls.env["res.partner"].create({"name": "Other Partner"})
        cls.acquirer = cls.env["payment.acquirer"].create(
            {"name": "Test Acquirer", "provider": "none", "state": "test"}
        )

    def _add_chatter(self, partner):
        message = partner.message_post(body="Chatter message")
        self.env["mail.tracking.value"].create(
            {
                "mail_message_id": message.id,
                "field": self.env["ir.model.fields"]._get("res.partner", "email").id,
                "field_desc": "Email",
                "field_type": "char",
                "old_value_char": "old@example.com",
                "new_value_char": "taro@example.com",
            }
        )
        partner.message_subscribe(partner_ids=self.other_partner.ids)
        partner.activity_schedule("mail.mail_activity_data_todo")
        self.env["ir.attachment"].create(
            {
                "name": "document.txt",
                "raw": b"personal data",
                "res_model": "res.partner",
                "res_id": partner.id,
            }
        )

    def _get_chatter(self, partners):
        domain = [("res_id", "in", partners.ids)]
        return {
            "mail.message": self.env["mail.message"].search(
                [("model", "=", "res.partner")] + domain
            ),
            "mail.tracking.value": self.env["mail.tracking.value"].search(
                [("mail_message_id.model", "=", "res.partner")]
                + [("mail_message_id.res_id", "in", partners.ids)]
            ),
            "mail.followers": self.env["mail.followers"].search(
                [("res_model", "=", "res.partner")] + domain
            ),
            "mail.activity": self.env["mail.activity"].search(
                [("res_model", "=", "res.partner")] + domain
            ),
            "ir.attachment": self.env["ir.attachment"].search(
                [("res_model", "=", "res.partner")] + domain
            ),
        }

    def _assert_anonymized(self, partner):
        self.assertEqual(partner.name, "退会済み %s" % partner.id)
        for field in (
            "email",
            "phone",
            "mobile",
            "street",
            "street2",
            "zip",
            "city",
            "state_id",
            "country_id",
            "furigana",
            "gender",
            "birthday",
            "image_1920",
        ):
            self.assertFalse(partner[field], "%s is not cleared" % field)
        self.assertEqual(partner.birth_month, 0)
        self.assertFalse(partner.active)

    def test_partner_anonymized(self):
        login = self.user.login
        self.user._deactivate_portal_account()
        self.assertFalse(
            self.env["res.users"]
            .with_context(active_test=False)
            .search([("login", "=", login)])
        )
        self._assert_anonymized(self.partner)
        self.assertEqual(self.partner.department, "Sales")
        self.assertEqual(self.partner.comment, "<p>Note kept after deactivation</p>")

    def test_child_contacts_anonymized(self):
        self.user._deactivate_portal_account()
        self._assert_anonymized(self.delivery)
        self._assert_anonymized(self.archived_delivery)

    def test_chatter_deleted(self):
        partners = self.partner | self.delivery
        for partner in partners | self.other_partner:
            self._add_chatter(partner)
        for model, records in self._get_chatter(partners).items():
            self.assertTrue(records, "No %s to delete in the test data" % model)
        self.user._deactivate_portal_account()
        for model, records in self._get_chatter(partners).items():
            self.assertFalse(records.exists(), "%s is not deleted" % model)
        for model, records in self._get_chatter(self.other_partner).items():
            self.assertTrue(records, "%s of another partner is deleted" % model)

    def test_payment_transaction_anonymized(self):
        tx = self.env["payment.transaction"].create(
            {
                "acquirer_id": self.acquirer.id,
                "reference": "TEST-DEACTIVATE",
                "amount": 1100.0,
                "currency_id": self.env.company.currency_id.id,
                "partner_id": self.partner.id,
                "state": "done",
            }
        )
        has_sale = "sale_order_ids" in tx._fields
        if has_sale:
            order = self.env["sale.order"].create({"partner_id": self.partner.id})
            tx.sale_order_ids = [Command.set(order.ids)]
        self.assertEqual(tx.partner_name, "Taro Yamada")
        self.assertEqual(tx.partner_email, "taro@example.com")
        create_date = tx.create_date
        self.user._deactivate_portal_account()
        for field in (
            "partner_name",
            "partner_email",
            "partner_phone",
            "partner_address",
            "partner_zip",
            "partner_city",
            "partner_state_id",
            "partner_country_id",
        ):
            self.assertFalse(tx[field], "%s is not cleared" % field)
        self.assertEqual(tx.partner_id, self.partner)
        self.assertEqual(tx.amount, 1100.0)
        self.assertEqual(tx.state, "done")
        self.assertEqual(tx.create_date, create_date)
        if has_sale:
            self.assertEqual(tx.sale_order_ids, order)

    def test_b2b_company_untouched(self):
        company = self.env["res.partner"].create(
            dict(
                self.address_vals,
                name="Test Company",
                is_company=True,
                email="info@example.com",
                phone="03-2222-2222",
            )
        )
        colleague = self.env["res.partner"].create(
            {
                "name": "Hanako Suzuki",
                "parent_id": company.id,
                "email": "hanako@example.com",
            }
        )
        company_delivery = self.env["res.partner"].create(
            dict(
                self.address_vals,
                name="Company Warehouse",
                parent_id=company.id,
                type="delivery",
            )
        )
        user = new_test_user(
            self.env, login="deactivate_b2b", groups="base.group_portal"
        )
        partner = user.partner_id
        partner.write({"parent_id": company.id, "email": "b2b@example.com"})
        untouched = company | colleague | company_delivery
        fields = ["name", "email", "phone", "street", "zip", "city", "active"]
        before = untouched.read(fields)
        user._deactivate_portal_account()
        self._assert_anonymized(partner)
        self.assertEqual(partner.parent_id, company)
        self.assertEqual(untouched.read(fields), before)
