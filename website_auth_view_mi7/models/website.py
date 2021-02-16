# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    login_page_header_text = fields.Html(
        "Login Page Header Text", translate=True, sanitize=False
    )
    login_page_signin_bottom_text = fields.Html(
        "Login Page Sign-in Bottom Text", translate=True, sanitize=False
    )
    login_page_signup_text = fields.Html(
        "Login Page User Register Text", translate=True, sanitize=False
    )
    signup_page_header_text = fields.Html(
        "Signup Page Header Text", translate=True, sanitize=False
    )
    signup_page_terms_text = fields.Html(
        "Signup Page Terms and Conditions Text", translate=True, sanitize=False
    )
    password_reset_page_header_text = fields.Html(
        "Password Reset Page Header Text", translate=True, sanitize=False
    )
