# -*- coding: utf-8 -*-
# Copyright 2021-2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, http
from odoo.http import request

from odoo.addons.website_portal.controllers.main import website_account


class WebsiteAccount(website_account):
    @http.route(["/my/account"], type="http", auth="user", website=True)
    def details(self, redirect=None, **post):
        old_email = request.env.user.partner_id.email
        response = super(WebsiteAccount, self).details(redirect=redirect, **post)
        if post and post["email"] and old_email != post["email"]:
            request.env.user._update_login_email(old_email, post["email"])
        return response

    def details_form_validate(self, data):
        error, error_message = super(WebsiteAccount, self).details_form_validate(data)
        if (
            "email" in data
            and data.get("email", False)
            and data.get("email", False) != request.env.user.login
        ):
            exist_user = (
                request.env["res.users"]
                .sudo()
                .search([("login", "=", data.get("email", False))])
            )
            if exist_user:
                error["email"] = "error"
                error_message.append(_("The email is already taken."))
        return error, error_message
