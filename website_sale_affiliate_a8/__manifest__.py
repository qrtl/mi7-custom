# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Sale Affiliate A8",
    "version": "15.0.1.1.0",
    "category": "Website",
    "website": "https://www.quartile.co",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["auth_signup_verify_email", "website_sale_delivery"],
    "data": [
        "data/data.xml",
        "views/res_partner_views.xml",
        "views/website_sale_templates.xml",
    ],
}
