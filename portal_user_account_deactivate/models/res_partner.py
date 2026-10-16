# Copyright 2026 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models

# A fixed value regardless of the language, so that staff can search for it.
ANONYMIZED_NAME = "退会済み %s"

PAYMENT_TRANSACTION_PERSONAL_FIELDS = [
    "partner_name",
    "partner_email",
    "partner_phone",
    "partner_address",
    "partner_zip",
    "partner_city",
    "partner_state_id",
    "partner_country_id",
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_account_deletion_vals(self):
        return {
            "email": False,
            "phone": False,
            "mobile": False,
            "street": False,
            "street2": False,
            "zip": False,
            "city": False,
            "state_id": False,
            "country_id": False,
            "furigana": False,
            "gender": False,
            "birthday": False,
            "image_1920": False,
            "active": False,
        }

    def _anonymize_for_account_deletion(self):
        """Erase the personal data of the partners and their child contacts.

        The parent company and sibling contacts of a B2B user are left untouched.
        Sales orders, invoices and their chatter are not modified, but the payment
        transactions keep only the amount, date, state and links to documents.
        """
        # Archived child contacts are included, but active_test must not stay False
        # on write, or the archived user would block archiving the partner.
        partners = (
            self.env["res.partner"]
            .sudo()
            .with_context(active_test=False)
            .search([("id", "child_of", self.ids)])
            .with_context(active_test=True, tracking_disable=True)
        )
        vals = self._get_account_deletion_vals()
        for partner in partners:
            partner.write(dict(vals, name=ANONYMIZED_NAME % partner.id))
        self.env["payment.transaction"].sudo().search(
            [("partner_id", "in", partners.ids)]
        ).write(dict.fromkeys(PAYMENT_TRANSACTION_PERSONAL_FIELDS, False))
        record_domain = [("res_id", "in", partners.ids)]
        self.env["mail.message"].sudo().search(
            [("model", "=", "res.partner")] + record_domain
        ).unlink()
        for model in ("mail.followers", "mail.activity", "ir.attachment"):
            self.env[model].sudo().search(
                [("res_model", "=", "res.partner")] + record_domain
            ).unlink()
