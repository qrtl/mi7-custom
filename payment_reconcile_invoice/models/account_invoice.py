# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_open(self):
        res = super(AccountInvoice, self).action_invoice_open()
        for invoice in self:
            if invoice.type != "out_invoice":
                continue
            orders = invoice.invoice_line_ids.mapped("sale_line_ids").mapped("order_id")
            for order in orders:
                tx = order.payment_tx_id
                if not tx:
                    continue
                payment = self.env["account.payment"].search(
                    [("payment_transaction_id", "=", tx.id)]
                )[:1]
                if not payment:
                    continue
                domain = [
                    ("account_id", "=", invoice.account_id.id),
                    (
                        "partner_id",
                        "=",
                        self.env["res.partner"]
                        ._find_accounting_partner(invoice.partner_id)
                        .id,
                    ),
                    ("reconciled", "=", False),
                    ("amount_residual", "!=", 0.0),
                    ("payment_id", "=", payment.id),
                    ("credit", ">", 0.0),
                    ("debit", "=", 0.0),
                ]
                line = self.env["account.move.line"].search(domain)[:1]
                if not line:
                    continue
                invoice.assign_outstanding_credit(line.id)
        return res
