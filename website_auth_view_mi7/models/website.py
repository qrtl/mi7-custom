# Copyright 2020-2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    login_page_header_text = fields.Html(translate=True, sanitize=False)
    login_page_signin_bottom_text = fields.Html(translate=True, sanitize=False)
    login_page_signup_text = fields.Html(translate=True, sanitize=False)
    signup_page_header_text = fields.Html(translate=True, sanitize=False)
    signup_page_terms_text = fields.Html(translate=True, sanitize=False)
    signup_page_bottom_text = fields.Html(translate=True, sanitize=False)
    password_reset_page_header_text = fields.Html(translate=True, sanitize=False)
