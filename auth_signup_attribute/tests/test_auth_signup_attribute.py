# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from lxml.html import document_fromstring

from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import HttpCase
from odoo.tools.misc import mute_logger

from odoo.addons.auth_signup_verify_email.controllers import main as verify_email
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
            "company_type": "person",
            "birthday": "1980-04-01",
        }

    def _get_csrf_token(self):
        doc = document_fromstring(self.url_open("/web/signup").content)
        return doc.xpath("//input[@name='csrf_token']")[0].get("value")

    def _signup(self):
        """Post the signup form and return the resulting HTML document.

        The email deliverability check and the mail sending are both patched
        out to keep the test independent from the network.
        """
        with patch.object(verify_email, "validate_email"), patch(
            mail_template.__name__ + ".MailTemplate.send_mail"
        ):
            response = self.url_open("/web/signup", data=self.data, timeout=30)
        return document_fromstring(response.content)

    def _get_partner(self):
        user = self.env["res.users"].search([("login", "=", self.data["login"])])
        return user.partner_id

    def _assert_rejected(self, doc):
        self.assertTrue(doc.xpath('//p[@class="alert alert-danger"]'))
        self.assertFalse(self._get_partner())

    @mute_logger("odoo.addons.auth_signup_verify_email.controllers.main")
    def test_signup_person(self):
        doc = self._signup()
        self.assertTrue(doc.xpath('//p[@class="alert alert-success"]'))
        partner = self._get_partner()
        self.assertFalse(partner.is_company)
        self.assertEqual(partner.birthday, fields.Date.to_date("1980-04-01"))

    @mute_logger("odoo.addons.auth_signup_verify_email.controllers.main")
    def test_signup_company(self):
        self.data["company_type"] = "company"
        # A date of birth left over from a switch to the company type is
        # discarded instead of being stored on a company.
        doc = self._signup()
        self.assertTrue(doc.xpath('//p[@class="alert alert-success"]'))
        partner = self._get_partner()
        self.assertTrue(partner.is_company)
        self.assertFalse(partner.birthday)

    @mute_logger("odoo.addons.auth_signup_verify_email.controllers.main")
    def test_signup_person_without_birthday(self):
        self.data["birthday"] = ""
        self._assert_rejected(self._signup())

    @mute_logger("odoo.addons.auth_signup_verify_email.controllers.main")
    def test_signup_person_with_invalid_birthday(self):
        # Anything the browser lets through is left to the ORM, which turns it
        # into the same generic error message as a missing date of birth.
        self.data["birthday"] = "not a date"
        doc = self._signup()
        self._assert_rejected(doc)
        # The posted value survives the re-render, so it does not have to be
        # filled in again.
        self.assertEqual(
            doc.xpath("//input[@name='birthday']")[0].get("value"), "not a date"
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
