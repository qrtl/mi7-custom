# Copyright 2026 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _unlock_linked_website_carts(self):
        self.mapped("sale_order_ids").action_unlock_website_cart()

    def _set_authorized(self, state_message=None):
        res = super()._set_authorized(state_message=state_message)
        self._unlock_linked_website_carts()
        return res

    def _set_done(self, state_message=None):
        res = super()._set_done(state_message=state_message)
        self._unlock_linked_website_carts()
        return res

    def _set_canceled(self, state_message=None):
        res = super()._set_canceled(state_message=state_message)
        self._unlock_linked_website_carts()
        return res

    def _set_error(self, state_message):
        res = super()._set_error(state_message=state_message)
        self._unlock_linked_website_carts()
        return res
