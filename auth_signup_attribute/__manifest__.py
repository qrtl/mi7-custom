# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Auth Signup Attribute",
    "summary": "Ask for the customer type and the date of birth at signup",
    "category": "Authentication",
    "version": "15.0.1.0.0",
    "author": "Quartile Limited",
    "maintainers": ["smorita7749"],
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": [
        "auth_signup_verify_email",
        "partner_attribute",
    ],
    "data": [
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "auth_signup_attribute/static/src/js/signup_attribute.js",
        ],
    },
    "installable": True,
}
