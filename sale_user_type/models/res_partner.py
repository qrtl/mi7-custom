# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    user_type = fields.Selection(
        [("b2c", "B2C"), ("b2b", "B2B")],
        "User Type",
        default="b2c",
        help="The setting of the parent is used for the sales order if there is a "
        "parent.",
    )
