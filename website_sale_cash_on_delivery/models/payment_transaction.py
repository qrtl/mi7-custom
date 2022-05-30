# -*- coding: utf-8 -*-
# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited

from odoo import models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _transfer_form_validate(self, data):
        if self.acquirer_id.is_cod and self.acquirer_id.auto_confirm in (
            "confirm_so",
            "generate_and_pay_invoice",
        ):
            if self.sale_order_id:
                tx = self
                self.sale_order_id.sudo().update_fee_line(tx)
            return self.write({"state": "done"})
        return super(PaymentTransaction, self)._transfer_form_validate(data)
