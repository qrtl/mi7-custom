# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    terms_agreed = fields.Boolean(
        tracking=True,
        copy=False,
        help="Indicates that the user has agreed to the terms and conditions at "
        "signup.",
    )
