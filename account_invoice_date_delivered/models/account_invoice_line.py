# -*- coding: utf-8 -*-
# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    time_delivered = fields.Datetime(related="invoice_id.time_delivered", store=True,)
    date_delivered = fields.Date(related="invoice_id.date_delivered", store=True,)
