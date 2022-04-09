# -*- coding: utf-8 -*-
# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import fields, models, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class ResPartner(models.Model):
    _inherit = "res.partner"

    furigana = fields.Char()
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")]
    )
    birthday = fields.Date(oldname="birth_date")
    birth_month = fields.Integer(
        "Birth Month",
        compute="_compute_birth_month",
        store=True,
        oldname="birth_date_month",
    )
    newsletter = fields.Selection(
        [("subscribe", "Subscribe"), ("unsubscribe", "Unsubscribe")],
        default="subscribe"
    )
    department = fields.Char("Department", oldname="department_name")

    @api.one
    @api.depends("birthday")
    def _compute_birth_month(self):
        if self.birthday:
            self.birth_month = int(datetime.strptime(self.birthday, DEFAULT_SERVER_DATE_FORMAT).strftime('%m'))
