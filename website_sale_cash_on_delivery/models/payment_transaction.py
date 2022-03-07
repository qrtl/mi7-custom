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
            return self.write({"state": "done"})
        return self.write({"state": "pending"})
