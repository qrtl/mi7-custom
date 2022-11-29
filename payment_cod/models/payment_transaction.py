# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _process_feedback_data(self, data):
        if not self.acquirer_id.is_cod:
            # We need to apply this condition before super() call unlike other
            # payment_xxx modules, since we use the 'transfer' provider, whose
            # _process_feedback_data() would call _set_pending() which would send out
            # a confirmation email, which we do not want here.
            super()._process_feedback_data(data)
            return
        if self.fees and self.sale_order_ids:
            # We assume that there is only one order for a payment transaction.
            fee_line = self.sale_order_ids[0].create_fee_line(self)
            # So that the tx amount matches the order amount.
            self.amount += fee_line.price_total
        self._set_done()

    def _finalize_post_processing(self):
        for tx in self:
            if tx.acquirer_id.is_cod:
                # We do not process payment and reconciliation by cron for COD cases.
                continue
            super(PaymentTransaction, tx)._finalize_post_processing()
        return
