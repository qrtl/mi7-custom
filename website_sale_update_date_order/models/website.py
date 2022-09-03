# -*- coding: utf-8 -*-
# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

from odoo import api, models, fields


class Website(models.Model):
    _inherit = "website"

    @api.multi
    def sale_get_order(
        self,
        force_create=False,
        code=None,
        update_pricelist=False,
        force_pricelist=False,
    ):
        """Extending the standard method to update date_order to the current date.
        This is to ensure that the correct pricing is applied when cart is updated,
        since the price computation in _get_display_price() uses date_order to look up
        the price.
        """
        order = super(Website, self).sale_get_order(
            force_create=force_create,
            code=code,
            update_pricelist=update_pricelist,
            force_pricelist=force_pricelist,
        )
        if order:
            date_order = datetime.strptime(order.date_order, DATETIME_FORMAT)
            date_order = fields.Datetime.context_timestamp(order, date_order).date()
            if fields.Date.to_string(date_order) != fields.Date.context_today(self):
                order.date_order = datetime.now()
        return order
