# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class WebsiteConfigSettings(models.TransientModel):
    _inherit = "website.config.settings"

    login_page_header_text = fields.Html(
        "Login Page Header Text", related="website_id.login_page_header_text"
    )
    login_page_signup_text = fields.Html(
        "Login Page User Register Text", related="website_id.login_page_signup_text"
    )
    signup_page_header_text = fields.Html(
        "Signup Page Header Text", related="website_id.signup_page_header_text"
    )
    signup_page_terms_text = fields.Html(
        "Signup Page Terms and Conditions Text",
        related="website_id.signup_page_terms_text",
    )
    password_reset_page_header_text = fields.Html(
        "Password Reset Page Header Text",
        related="website_id.password_reset_page_header_text",
    )
