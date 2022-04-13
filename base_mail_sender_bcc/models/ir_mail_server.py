# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    def build_email(
        self,
        email_from,
        email_to,
        subject,
        body,
        email_cc=None,
        email_bcc=None,
        reply_to=False,
        attachments=None,
        message_id=None,
        references=None,
        object_id=False,
        subtype="plain",
        headers=None,
        body_alternative=None,
        subtype_alternative="plain",
    ):
        if reply_to:
            email_bcc = [reply_to]
        else:
            email_bcc_parameter = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("email_bcc", default=False)
            )
            if email_bcc_parameter:
                if email_bcc is None:
                    email_bcc = [email_bcc_parameter]
                elif (
                    isinstance(email_bcc, list) and email_bcc_parameter not in email_bcc
                ):
                    email_bcc.append(email_bcc_parameter)
        return super(IrMailServer, self).build_email(
            email_from,
            email_to,
            subject,
            body,
            email_cc=email_cc,
            email_bcc=email_bcc,
            reply_to=reply_to,
            attachments=attachments,
            message_id=message_id,
            references=references,
            object_id=object_id,
            subtype=subtype,
            headers=headers,
            body_alternative=body_alternative,
            subtype_alternative=subtype_alternative,
        )
