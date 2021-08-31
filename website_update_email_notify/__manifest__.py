# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Portal Login Change",
    "category": "Website",
    "license": "LGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "version": "10.0.1.0.0",
    # Need to have "pro_mi7_website_sale_ec" as a dependency,
    # since this module overrides the detail() controller:
    # https://github.com/qrtl/pro-mi7/blob/2a6f015f8928fb5748052ac819dbc04dff0ae4b5/pro_mi7_website_sale_ec/controllers/website_portal_main.py#L71-L107 # noqa
    "depends": ["mail", "pro_mi7_website_sale_ec"],
    "data": ["views/templates.xml", "views/email_templates.xml"],
    "installable": True,
}
