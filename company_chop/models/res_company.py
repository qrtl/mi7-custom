# -*- coding: utf-8 -*-
# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    company_chop = fields.Binary("Company Chop", attachment=True, oldname="stamp_image")
