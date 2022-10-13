# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from odoo import api
from odoo.http import request, route

from odoo.addons.auth_signup_verify_email.controllers.main import SignupVerifyEmail
from odoo.addons.website_sale.controllers.main import WebsiteSale


class SignupVerifyEmail(SignupVerifyEmail):
    @api.model
    def _write_a8_param_to_user(self, user, cookie_a8):
        # A8 param should be effective for 90 days.
        expiry_date = datetime.today() + timedelta(days=90)
        user.write({"a8_param": cookie_a8, "a8_expiry_date": expiry_date})

    @route()
    def web_login(self, *args, **kw):
        res = super().web_login(*args, **kw)
        if request.httprequest.method == "POST":
            cookie_a8 = request.httprequest.cookies.get(request.website.a8_cookie_key)
            if not cookie_a8:
                return res
            # TODO: Not sure we could simply use request.env.user depending on the res
            # status
            uid = request.session.authenticate(
                request.session.db, request.params["login"], request.params["password"]
            )
            if uid is not False:
                user = request.env["res.users"].sudo().search([("id", "=", uid)])
                self._write_a8_param_to_user(user, cookie_a8)
        return res

    def passwordless_signup(self):
        res = super().passwordless_signup()
        cookie_a8 = request.httprequest.cookies.get(request.website.a8_cookie_key)
        if not cookie_a8:
            return res
        login = res.qcontext.get("login")
        user = request.env["res.users"].sudo().search([("login", "=", login)])
        if user:
            self._write_a8_param_to_user(user, cookie_a8)
        return res


class WebsiteSale(WebsiteSale):
    @route()
    def checkout(self, **post):
        """Cookie needs to exist in user's device to be able to record the sales with
        A8.
        """
        res = super().checkout(**post)
        cookie_a8 = request.httprequest.cookies.get(request.website.a8_cookie_key)
        if cookie_a8:
            return res
        # If a8_param exists and cookie does not, then create a cookie.
        user = request.env.user
        if (
            user.a8_param
            and user.a8_expiry_date
            and user.a8_expiry_date >= datetime.today()
        ):
            res.set_cookie(
                request.website.a8_cookie_key,
                value=user.a8_param,
                expires=datetime.strftime(
                    user.a8_expiry_date, "%a, %d-%b-%Y %H:%M:%S GMT"
                ),
                path="/",
            )
        return res

    @route()
    def shop_payment_confirmation(self, **post):
        res = super().shop_payment_confirmation(**post)
        user = request.env.user
        # Existing a8_param should be deleted upon a purchase.
        if user.a8_param:
            user.write({"a8_param": False, "a8_expiry_date": False})
        return res
