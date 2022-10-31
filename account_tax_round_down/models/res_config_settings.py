# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    need_tax_round_down = fields.Boolean(
        related="company_id.need_tax_round_down",
        readonly=False,
    )
