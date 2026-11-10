# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from lxml.html import document_fromstring

from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.mail.models import mail_template


@tagged("post_install", "-at_install")
class TestAuthSignupAttribute(HttpCase):
    def setUp(self):
        super().setUp()
        if "website" in self.env:
            self.env["website"].get_current_website().auth_signup_uninvited = "b2c"
        self.env["ir.config_parameter"].set_param("auth_signup.invitation_scope", "b2c")
        self.data = {
            "csrf_token": self._get_csrf_token(),
            "name": "Somebody",
            "login": "somebody@example.com",
            "password": "Passw0rd!",
            "confirm_password": "Passw0rd!",
            "company_type": "person",
            "birthday": "1980-04-01",
        }

    def _get_csrf_token(self):
        doc = document_fromstring(self.url_open("/web/signup").content)
        return doc.xpath("//input[@name='csrf_token']")[0].get("value")

    def _signup(self):
        """Post the signup form and return the resulting HTML document.

        The account creation mail is patched out to keep the test independent
        from the network.
        """
        with patch(mail_template.__name__ + ".MailTemplate.send_mail"):
            response = self.url_open("/web/signup", data=self.data, timeout=30)
        return document_fromstring(response.content)

    def _get_partner(self):
        user = self.env["res.users"].search([("login", "=", self.data["login"])])
        return user.partner_id

    def test_signup_person(self):
        self._signup()
        partner = self._get_partner()
        self.assertFalse(partner.is_company)
        self.assertEqual(partner.birthday, fields.Date.to_date("1980-04-01"))

    def test_signup_company(self):
        self.data["company_type"] = "company"
        # A date of birth left over from a switch to the company type is
        # discarded instead of being stored on a company.
        self._signup()
        partner = self._get_partner()
        self.assertTrue(partner.is_company)
        self.assertFalse(partner.birthday)

    def test_signup_person_without_birthday(self):
        self.data["birthday"] = ""
        doc = self._signup()
        self.assertFalse(self._get_partner())
        self.assertIn(
            "Please enter your date of birth.",
            doc.xpath('//p[@class="alert alert-danger"]')[0].text_content(),
        )

    def test_signup_other_error_keeps_its_message(self):
        """A failure that is not about the date of birth keeps its own message.

        The message of the model is recovered in the template, so it must not
        be applied to a rejection that happened for another reason.
        """
        self.data["confirm_password"] = "Different!"
        self.data["birthday"] = ""
        doc = self._signup()
        self.assertFalse(self._get_partner())
        self.assertIn(
            "Passwords do not match",
            doc.xpath('//p[@class="alert alert-danger"]')[0].text_content(),
        )

    def test_signup_invited(self):
        """An invited signup carries no attributes and must not be blocked."""
        partner = self.env["res.partner"].create({"name": "Invited"})
        partner.signup_prepare()
        self.data = {
            "csrf_token": self.data["csrf_token"],
            "token": partner.signup_token,
            "login": "invited@example.com",
            "name": partner.name,
            "password": "Passw0rd!",
            "confirm_password": "Passw0rd!",
        }
        doc = self._signup()
        self.assertFalse(doc.xpath('//p[@class="alert alert-danger"]'))
        self.assertTrue(partner.user_ids)
