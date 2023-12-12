# Copyright 2023 Quartile Limited

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for order in self:
            tx = order.sudo().transaction_ids._get_last()
            if not tx:
                continue
            if tx.acquirer_id.is_cod:
                payment_term = order.env.ref(
                    "payment_cod_payment_term.account_payment_term_cod"
                )
                order.write({"payment_term_id": payment_term.id})
        return super().action_confirm()
