# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class MailMessage(models.Model):
    _inherit = "mail.message"

    @api.model
    def create(self, vals):
        if vals.get("message_type") == "comment":
            subtype = self.env["mail.message.subtype"].browse(vals.get("subtype_id"))
            if (
                vals.get("model") not in subtype.allow_send_model_ids.mapped("model")
                and not subtype.internal
            ):
                raise ValidationError(
                    _("You are going to send an email to external, message blocked!")
                )
        return super(MailMessage, self).create(vals)
