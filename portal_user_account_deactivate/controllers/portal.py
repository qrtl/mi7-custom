# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID
from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal as Portal


class CustomerPortal(Portal):
    @route()
    def security(self, **post):
        response = super().security(**post)
        response.qcontext[
            "can_deactivate_account"
        ] = request.env.user._can_deactivate_portal_account()
        return response

    @route("/my/deactivate", type="http", auth="user", website=True, methods=["POST"])
    def deactivate_account(self, **post):
        user = request.env.user
        if not user._can_deactivate_portal_account():
            return request.redirect("/my/security")
        user.with_user(SUPERUSER_ID)._deactivate_portal_account()
        return request.redirect("/web")
