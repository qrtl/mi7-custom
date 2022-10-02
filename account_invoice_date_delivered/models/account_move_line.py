# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    time_delivered = fields.Datetime(
        related="move_id.time_delivered",
        store=True,
    )
    date_delivered = fields.Date(
        related="move_id.date_delivered",
        store=True,
    )
