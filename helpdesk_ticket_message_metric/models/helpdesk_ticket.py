# Copyright 2025 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    first_reply_date = fields.Datetime(
        compute="_compute_first_reply_date",
        store=True,
        help="Date of the first reply sent to the customer by an internal user.",
    )
    interaction_count = fields.Integer(
        compute="_compute_interaction_count",
        store=True,
    )

    @api.depends("message_ids")
    def _compute_first_reply_date(self):
        for ticket in self:
            messages = ticket.message_ids.filtered(
                lambda m: m.message_type in ("email", "comment")
                and not m.subtype_id.internal
                and m.author_id != ticket.partner_id
                and m.author_id.user_ids.filtered(lambda u: not u.share)
            ).sorted("date")
            ticket.first_reply_date = messages[0].date if messages else False

    @api.depends("message_ids")
    def _compute_interaction_count(self):
        for ticket in self:
            ticket.interaction_count = len(
                ticket.message_ids.filtered(
                    lambda m: m.message_type in ("email", "comment")
                    and not m.subtype_id.internal
                )
            )
