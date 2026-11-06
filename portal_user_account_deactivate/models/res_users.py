# Copyright 2026 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    def _can_deactivate_portal_account(self):
        """Return whether the user can deactivate their account from the portal."""
        self.ensure_one()
        partner = self.partner_id
        if partner.user_type == "b2b":
            return False
        # The checks below keep the deactivation from failing or reaching other
        # people's records when user_type is wrong.
        if partner.parent_id and partner.type != "contact":
            return False
        descendants = (
            self.env["res.partner"]
            .sudo()
            .with_context(active_test=False)
            .search([("id", "child_of", partner.ids), ("id", "!=", partner.id)])
        )
        if descendants.filtered(lambda p: p.type == "contact"):
            return False
        return (
            not self.env["res.users"]
            .sudo()
            .search_count(
                [
                    ("partner_id", "in", (partner | descendants).ids),
                    ("id", "!=", self.id),
                ]
            )
        )

    def _deactivate_portal_account(self):
        if not all(user._can_deactivate_portal_account() for user in self):
            raise UserError(_("This account cannot be deactivated."))
        # The user must be archived first, as a partner linked to an active user
        # cannot be archived.
        self.write({"active": False})
        self.partner_id._anonymize_for_account_deletion()
        self.unlink()
