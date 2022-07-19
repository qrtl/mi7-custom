# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    error_msg = fields.Html(
        string="Error Message",
        help="The message displayed if there has been an error during the payment process",
        translate=True,
    )
    show_error_msg = fields.Boolean(compute="_compute_show_error_msg")

    @api.depends("provider")
    def _compute_show_error_msg(self):
        """The value is set to `False` by default."""
        self.update({"show_error_msg": False})
