# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _get_factor(self):
        self.ensure_one()
        if self.type in ("out_invoice", "in_invoice"):
            return 1
        return -1
