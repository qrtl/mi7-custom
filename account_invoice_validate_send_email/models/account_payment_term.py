# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    not_send_invoice = fields.Boolean(
        string="Not Auto-send Invoice",
        help="When this field is selected, no email will be automatically sent to the customer despite the settings of the linked workflow process.",
    )
