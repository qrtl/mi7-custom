# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.multi
    def get_mail_values(self, res_ids):
        self.ensure_one()
        results = super(MailComposeMessage, self).get_mail_values(res_ids)
        reply_to = self.reply_to
        for res_id in res_ids:
            results[res_id]["reply_to"] = reply_to
        return results
