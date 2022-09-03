# -*- coding: utf-8 -*-
# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _cart_update(
        self,
        product_id=None,
        line_id=None,
        add_qty=0,
        set_qty=0,
        attributes=None,
        **kwargs
    ):
        """Extending the standard method to update date_order to the current date.
        This is to ensure that the correct pricing is applied when cart is updated,
        since the price computation in _get_display_price() uses date_order to look up
        the price.
        """
        self.ensure_one()
        date_order = datetime.strptime(self.date_order, DATETIME_FORMAT)
        date_order = fields.Datetime.context_timestamp(self, date_order).date()
        if fields.Date.to_string(date_order) != fields.Date.context_today(self):
            self.date_order = datetime.now()
        return super(SaleOrder, self)._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            attributes=attributes,
            **kwargs,
        )
