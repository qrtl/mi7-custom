# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    account_delete_caution_text = fields.Text(
        translate=True,
        help="This text shows in the Deactivate Account section of /my/security page.",
    )
