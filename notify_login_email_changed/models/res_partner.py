# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _send_email(self, mail_template, old_email="", new_email=""):
        self.ensure_one()
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

    def write(self, vals):
        if vals.get("email"):
            mail_ex_id =\
                "notify_login_email_changed.email_template_notify_email_change"
            mail_template = self.env.ref(mail_ex_id)
            new_email = vals["email"]
            for partner in self:
                partner._send_email(mail_template, partner.email, new_email)

        return super(ResPartner, self).write(vals)
