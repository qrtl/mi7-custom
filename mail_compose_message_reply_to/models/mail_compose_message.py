# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailComposeMessageReplyTo(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.multi
    def get_mail_values(self, res_ids):
        self.ensure_one()
        results = super(MailComposeMessageReplyTo, self).get_mail_values(res_ids)
        for res_id in res_ids:
            if (
                self.reply_to
                and "reply_to" not in results[res_id]
                and "@" not in results[res_id]["reply_to"]
            ):
                results[res_id]["reply_to"] = self.reply_to
        return results
