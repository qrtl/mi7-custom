# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, tools


class Currency(models.Model):
    _inherit = "res.currency"

    def round(self, amount):
        self.ensure_one()
        if "rounding_method" in self._context:
            return tools.float_round(
                amount,
                precision_rounding=self.rounding,
                rounding_method=self._context.get("rounding_method"),
            )
        return super().round(amount)
