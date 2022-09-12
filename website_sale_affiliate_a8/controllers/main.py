# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from odoo import fields
from odoo.http import request, route

from odoo.addons.auth_signup_verify_email.controllers.main import SignupVerifyEmail
from odoo.addons.website_sale.controllers.main import WebsiteSale


class SignupVerifyEmail(SignupVerifyEmail):
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
                # A8 param should be effective for 90 days.
                user.write(
                    {
                        "a8_param": cookie_a8,
                        "a8_expiry_date": fields.Datetime.from_string(
                            fields.Date.context_today(user)
                        )
                        + timedelta(days=90),
                    }
                )
        return res

    def passwordless_signup(self):
        res = super().passwordless_signup()
        cookie_a8 = request.httprequest.cookies.get(request.website.a8_cookie_key)
        if not cookie_a8:
            return res
        login = res.qcontext.get("login")
        user = request.env["res.users"].sudo().search([("login", "=", login)])
        if user:
            # A8 param should be effective for 90 days.
            user.write(
                {
                    "a8_param": cookie_a8,
                    "a8_expiry_date": fields.Datetime.from_string(
                        fields.Date.context_today(user)
                    )
                    + timedelta(days=90),
                }
            )
        return res


class WebsiteSale(WebsiteSale):
    @route()
    def checkout(self, **post):
        """Cookie needs to exist in user's device to be able to record the sales with
        A8.
        """
        res = super().checkout(**post)
        user = request.env.user
        cookie_a8 = request.httprequest.cookies.get(request.website.a8_cookie_key)
        # When the a8_param exist and cookie doesn't exist, set cookie.
        if cookie_a8:
            return res
        user = request.env.user
        if (
            user.a8_param
            and user.a8_expiry_date
            and user.a8_expiry_date >= fields.Date.context_today(user)
        ):
            res.set_cookie(
                request.website.a8_cookie_key,
                value=user.a8_param,
                max_age=user.a8_expiry_date,
                expires=user.a8_expiry_date,
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
