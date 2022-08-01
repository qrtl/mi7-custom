# Copyright 2022 Quartile Limited

from odoo import fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    is_cod = fields.Boolean("Cash on Delivery")
    amount_limit = fields.Monetary("Amount Limit")
    currency_id = fields.Many2one(related="company_id.currency_id")
