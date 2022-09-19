# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    need_tax_round_down = fields.Boolean(
        default=True,
        help="If selected, rounding method 'DOWN' will be applied to tax amounts.",
    )
