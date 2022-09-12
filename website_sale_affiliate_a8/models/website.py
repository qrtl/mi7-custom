# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    a8_cookie_key = fields.Char(
        "A8 Cookie Key",
        help="The key of the cookie used for the A8 JS-Tag method.",
        compute="_compute_a8_cookie_key",
    )

    @api.multi
    def _compute_a8_cookie_key(self):
        a8_pid = self.env["ir.config_parameter"].sudo().get_param("affiliate.pid")
        if a8_pid:
            for website in self:
                website.a8_cookie_key = "_a8_" + a8_pid
