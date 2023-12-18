# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    send_invoice = fields.Boolean(related="workflow_process_id.send_invoice")
    invoice_sent = fields.Boolean(
        # readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
        help="When this field is selected, no email will be automatically sent to the "
        "customer.",
    )
    carrier_tracking_refs = fields.Char(
        "Tracking References",
        help="Delivery slip numbers taken from the linked deliveries.",
        compute="_compute_carrier_info",
    )
    carrier_info_name = fields.Char(compute="_compute_carrier_info")
    carrier_tracking_url = fields.Char(compute="_compute_carrier_info")

    def _get_mail_template(self):
        self.ensure_one()
        template = False
        if self.commercial_partner_id.user_type == "b2b":
            template = self.company_id.invoice_mail_template_id
        elif self.commercial_partner_id.user_type == "b2c":
            template = self.company_id.invoice_mail_template_b2c_id
        if not template:
            return super()._get_mail_template()
        model_data_rec = self.env["ir.model.data"].search(
            [("model", "=", "mail.template"), ("res_id", "=", template.id)]
        )
        if not model_data_rec:
            return super()._get_mail_template()
        return model_data_rec.complete_name

    def action_send_invoice(self):
        self.ensure_one()
        email_act = self.action_invoice_sent()
        if email_act and email_act.get("context"):
            email_ctx = email_act["context"]
            self.with_context(**email_ctx).message_post_with_template(
                email_ctx.get("default_template_id")
            )
            self.invoice_sent = True
        return True

    def action_post(self):
        res = super().action_post()
        for move in self:
            if move.move_type != "out_invoice":
                continue
            if not move.send_invoice or move.invoice_sent:
                continue
            term = move.invoice_payment_term_id
            if term and term.not_send_invoice:
                continue
            pickings = move.picking_ids
            if not pickings or pickings.filtered(lambda x: x.not_send_invoice):
                continue
            # Skip sending invoice if the invoice is not physical and the customer is B2C.
            if (
                move.commercial_partner_id.user_type == "b2c"
                and not move.invoice_line_ids.filtered(
                    lambda x: x.product_id.is_physical
                )
            ):
                continue
            move.action_send_invoice()
        return res

    def _compute_carrier_info(self):
        for move in self:
            move.carrier_info_name = ""
            move.carrier_tracking_url = ""
            move.carrier_tracking_refs = ""
            if move.move_type != "out_invoice":
                continue
            carrier_recs = move.picking_ids.mapped("carrier_info_id").filtered(
                lambda x: not x.is_dummy
            )
            if carrier_recs:
                move.carrier_info_name = ", ".join(x.name for x in carrier_recs)
                tracking_urls = carrier_recs.mapped("tracking_url")
                if tracking_urls:
                    move.carrier_tracking_url = ", ".join(
                        url for url in tracking_urls if url
                    )
            tracking_refs = []
            for pick in move.picking_ids:
                if pick.carrier_tracking_ref:
                    tracking_refs.append(pick.carrier_tracking_ref)
            if tracking_refs:
                move.carrier_tracking_refs = ", ".join(tracking_refs)
