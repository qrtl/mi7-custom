# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID
from odoo.http import request, route

from odoo.addons.portal.controllers.portal import CustomerPortal as Portal


class CustomerPortal(Portal):
    @route("/my/deactivate", type="http", auth="user", website=True, methods=["POST"])
    def deactivate_account(self, **post):
        user = request.env.user
        if user:
            user.with_user(SUPERUSER_ID).write({"active": False})
            user.partner_id.with_user(SUPERUSER_ID).write({"active": False})
            return request.redirect("/web")
