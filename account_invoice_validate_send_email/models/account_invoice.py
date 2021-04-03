# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    invoice_sent = fields.Boolean(
        string="Invoice Sent",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="When this field is selected, no email will be automatically sent to the customer.",
    )
    web_url = fields.Char()

    def _get_mail_template_id(self):
        try:
            res = self.env.ref(
                "account_invoice_validate_send_email.email_template_customer_invoice_validated"
            ).id
        except ValueError:
            res = False
        return res

    @api.multi
    def get_mail_compose_message(self):
        self.ensure_one()
        template_id = self._get_mail_template_id()
        try:
            compose_form_id = self.env.ref("mail.email_compose_message_wizard_form").id
        except ValueError:
            compose_form_id = False
        ctx = dict(
            mark_invoice_as_sent=True,
            # We choose not to use the custom layout here for now.
            # custom_layout="account.mail_template_data_notification_email_account_invoice",
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

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()
        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        for invoice in self:
            if (
                invoice.workflow_process_id
                and invoice.workflow_process_id.send_invoice
                and not invoice.invoice_sent
            ):
                # TODO We may want to adjust/remove web_url - the value points
                # to the standard report which is not what we want to print
                # now, and as a result we are not using this field for the time
                # being.
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
                self.invoice_sent = True
        return True
