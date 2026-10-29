# Copyright 2026 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


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

    def _get_payment_transaction_deletion_vals(self):
        return {
            "partner_name": False,
            "partner_email": False,
            "partner_phone": False,
            "partner_address": False,
            "partner_zip": False,
            "partner_city": False,
            "partner_state_id": False,
            "partner_country_id": False,
        }

    def _anonymize_for_account_deletion(self):
        """Anonymize the partners and their child contacts.

        Clear their personal data, rename them to "退会済み <ID>", clear the
        customer details on their payment transactions, and delete their messages,
        followers, activities and attachments.
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
            # Not translated, so that staff can search for it in any language.
            partner.write(dict(vals, name="退会済み %s" % partner.id))
        self.env["payment.transaction"].sudo().search(
            [("partner_id", "in", partners.ids)]
        ).write(self._get_payment_transaction_deletion_vals())
        record_domain = [("res_id", "in", partners.ids)]
        self.env["mail.message"].sudo().search(
            [("model", "=", "res.partner")] + record_domain
        ).unlink()
        for model in ("mail.followers", "mail.activity", "ir.attachment"):
            self.env[model].sudo().search(
                [("res_model", "=", "res.partner")] + record_domain
            ).unlink()
