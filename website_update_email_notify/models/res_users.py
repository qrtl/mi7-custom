# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _update_login_email(self, old_email, new_email):
        self.ensure_one()
        self.sudo().update({"login": new_email})
        mail_template = self.env.ref(
            "website_update_email_notify.email_template_notify_email_change"
        )
        ctx = {
            "mail_create_nosubscribe": True,
            "disable_message_subscribe": True,
            "old_email": old_email,
            "new_email": new_email,
        }
        self.partner_id.with_context(ctx).message_post_with_template(mail_template.id)
