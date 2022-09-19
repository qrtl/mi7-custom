# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountTax(models.Model):
    _inherit = "account.tax"

    # This adjustment also affects the tax-inclusive price presentation in the eCommerce
    # shop.
    def compute_all(
        self,
        price_unit,
        currency=None,
        quantity=1.0,
        product=None,
        partner=None,
        is_refund=False,
        handle_price_include=True,
        include_caba_tags=False,
    ):
        if not self:
            company = self.env.company
        else:
            company = self[0].company_id
        if company.need_tax_round_down:
            rounding_method = "DOWN"
            if self.mapped("price_include") == [True]:
                # In case all taxes have 'Included in Price' selected, then we reverse
                # the rounding method, since the excluded amount is calculated first,
                # and then the tax amount is calculated by subtracting the excluded
                # amount from the total.
                # We cannot cover the pattern where multiple taxes with different
                # price_include settings are involved due to the structure of
                # compute_all() method.
                rounding_method = "UP"
            # This matters when currency is NOT given
            self = self.with_context(rounding_method=rounding_method)
            # This matters when currency is given
            currency = currency.with_context(rounding_method=rounding_method)
        return super().compute_all(
            price_unit,
            currency=currency,
            quantity=quantity,
            product=product,
            partner=partner,
            is_refund=is_refund,
            handle_price_include=handle_price_include,
            include_caba_tags=include_caba_tags,
        )
