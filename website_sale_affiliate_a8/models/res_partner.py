# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    a8_param = fields.Char("A8 Identification Parameter", copy=False)
    a8_expiry_date = fields.Date("A8 Expiry Date", copy=False)
