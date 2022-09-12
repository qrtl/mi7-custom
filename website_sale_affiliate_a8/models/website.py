# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    a8_cookie_key = fields.Char(
        help="The key of the cookie used for the A8 JS-tag method.",
        compute="_compute_a8_cookie_key",
    )

    def _compute_a8_cookie_key(self):
        # TODO: should A8 PID be moved to website, especially when other website shops
        # open?
        a8_pid = self.env["ir.config_parameter"].sudo().get_param("affiliate.pid")
        for website in self:
            if a8_pid:
                website.a8_cookie_key = "_a8_" + a8_pid
            else:
                website.a8_cookie_key = False
