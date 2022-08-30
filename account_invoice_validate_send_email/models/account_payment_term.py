# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    not_send_invoice = fields.Boolean(
        string="Not Auto-send Invoice",
        help="When this field is selected, the invoices that use this payment "
        "term will be outside the scope of automated invoice email despite "
        "the settings of the linked workflow process.",
    )
