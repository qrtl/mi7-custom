# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    send_invoice = fields.Boolean(related="workflow_process_id.send_invoice")
    invoice_sent = fields.Boolean(
        string="Invoice Sent",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
        help="When this field is selected, no email will be automatically sent to the customer.",
    )
    web_url = fields.Char()

    def _get_mail_template(self):
        self.ensure_one()
        if self.company_id.invoice_mail_template_id:
            return self.company_id.invoice_mail_template_id
        else:
            return False

    @api.multi
    def get_mail_compose_message(self):
        self.ensure_one()
        template = self._get_mail_template()
        if not template:
            raise UserError(_("company_id cannot detect"))
        try:
            compose_form_id = self.env.ref("mail.email_compose_message_wizard_form").id
        except ValueError:
            compose_form_id = False
        ctx = dict(
            mark_invoice_as_sent=True,
            # We choose to use the custom layout here, or there will be a link
            # button to the backend form.
            custom_layout="account.mail_template_data_notification_email_account_invoice",
        )
        ctx.update(
            {
                "default_model": "account.invoice",
                "default_res_id": self.ids[0],
                "default_use_template": bool(template),
                "default_template_id": template.id,
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
            term = invoice.payment_term_id
            if (
                invoice.send_invoice
                and not (term and term.not_send_invoice)
                and not invoice.picking_ids.filtered(lambda x: x.not_send_invoice)
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
        if self.type in ("out_invoice", "out_refund"):
            email_act = self.get_mail_compose_message()
            if email_act and email_act.get("context"):
                email_ctx = email_act["context"]
                self.with_context(email_ctx).message_post_with_template(
                    email_ctx.get("default_template_id")
                )
                self.invoice_sent = True
        return True
