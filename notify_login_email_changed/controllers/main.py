# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request

from odoo.addons.website_portal.controllers.main import website_account


class WebsiteAccount(website_account):
    @http.route(["/my/account"], type="http", auth="user", website=True)
    def details(self, redirect=None, **post):
        partner = request.env.user.partner_id
        old_email = partner.email
        response = super(WebsiteAccount, self).details(redirect=redirect, **post)
        if post and post["email"] and old_email != post["email"]:
            partner._update_login_email(post["email"])
            partner._send_email(old_email, post["email"])
        return response
