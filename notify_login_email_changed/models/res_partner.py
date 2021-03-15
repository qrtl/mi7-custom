# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _send_email(self, old_email="", new_email=""):
        self.ensure_one()
        module = "notify_login_email_changed"
        mail_ex_id = "email_template_notify_email_change"
        mail_template = self.env.ref("{}.{}".format(module, mail_ex_id))

        ctx = {
            "default_composition_mode": "comment",
            "mail_create_nosubscribe": True,
            "disable_message_subscribe": True,
            "template_type": "comment",
            "old_email": old_email,
            "new_email": new_email,
        }
        template = mail_template.with_context(ctx)
        template.send_mail(self.id, force_send=True)
        return True
