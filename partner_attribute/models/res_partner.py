# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ResPartner(models.Model):
    _inherit = "res.partner"

    furigana = fields.Char()
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")]
    )
    birthday = fields.Date()
    birth_month = fields.Integer(
        compute="_compute_birth_month",
        store=True,
    )
    newsletter = fields.Selection(
        [("subscribe", "Subscribe"), ("unsubscribe", "Unsubscribe")],
        default="subscribe",
    )
    department = fields.Char()

    @api.depends("birthday")
    def _compute_birth_month(self):
        for partner in self:
            if partner.birthday:
                partner.birth_month = int(
                    datetime.strptime(
                        str(partner.birthday), DEFAULT_SERVER_DATE_FORMAT
                    ).strftime("%m")
                )
