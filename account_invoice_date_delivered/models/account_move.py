# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from datetime import date

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

from odoo.addons.base_timezone_converter.tools.tz_utils import convert_datetime_from_utc

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    time_delivered = fields.Datetime(
        compute="_compute_date_delivered",
        string="Delivered Time",
        store=True,
    )
    date_delivered = fields.Date(
        compute="_compute_date_delivered",
        string="Delivered Date",
        store=True,
    )

    @api.depends("picking_ids", "picking_ids.date_done")
    def _compute_date_delivered(self):
        DATE_LENGTH = len(date.today().strftime(DATE_FORMAT))
        for invoice in self:
            invoice.time_delivered = False
            invoice.date_delivered = False
            if invoice.move_type not in ("out_invoice", "out_refund"):
                continue
            # We assume that there will not be multiple pickings per invoice.
            pick = invoice.picking_ids[:1]
            if not pick or not pick.date_done:
                continue
            _logger.info("_compute_date_delivered(): %s" % invoice.name)
            invoice.time_delivered = pick.date_done
            time_delivered = convert_datetime_from_utc(pick.date_done, self.env.user.tz)
            time_delivered = fields.Datetime.to_string(time_delivered)
            invoice.date_delivered = time_delivered[:DATE_LENGTH]
