# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    need_tax_round_down = fields.Boolean(
        related="company_id.need_tax_round_down",
        readonly=False,
    )
