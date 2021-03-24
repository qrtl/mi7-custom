# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    invoice_sent = fields.Boolean(default=False)
    web_url = fields.Char()

    @api.multi
    def action_invoice_draft(self):
        res = super(AccountInvoice, self).action_invoice_draft()
        self.update({"invoice_sent": False})
        return res

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()
        self.update({"invoice_sent": True})
        for invoice in self:
            base_url = self.env["ir.config_parameter"].get_param("web.base.url")
            invoice.web_url = base_url + "/my/invoices/pdf/" + str(invoice.id)
            invoice.action_send()
        return res

    @api.multi
    def action_send(self):
        # send notification email for follower
        self.ensure_one()
        if self.type == "out_invoice":
            email_act = self.get_mail_compose_message()
            if email_act and email_act.get("context"):
                email_ctx = email_act["context"]
                self.with_context(email_ctx).message_post_with_template(
                    email_ctx.get("default_template_id")
                )
        return True

    @api.multi
    def get_mail_compose_message(self):
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            template_id = ir_model_data.get_object_reference(
                "account_invoice_auto_dispatch",
                "email_template_customer_invoice_validated",
            )[1]
        except ValueError:
            template_id = False

        try:
            compose_form_id = ir_model_data.get_object_reference(
                "mail", "email_compose_message_wizard_form"
            )[1]
        except ValueError:
            compose_form_id = False

        ctx = dict(
            mark_invoice_as_sent=True,
            custom_layout="account.mail_template_data_notification_email_account_invoice",
        )
        ctx.update(
            {
                "default_model": "account.invoice",
                "default_res_id": self.ids[0],
                "default_use_template": bool(template_id),
                "default_template_id": template_id,
                "default_composition_mode": "comment",
                "notify_partner_ids": ",".join(
                    [str(partner_id) for partner_id in self.message_partner_ids.ids]
                ),
            }
        )
        return {
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form_id, "form")],
            "view_id": compose_form_id,
            "target": "new",
            "context": ctx,
        }
