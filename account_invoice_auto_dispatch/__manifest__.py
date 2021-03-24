# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Account Invoice Notification",
    "category": "Accouting",
    "license": "LGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "version": "10.0.1.0.0",
    "depends": ["account", "website_portal_sale"],
    "data": ["views/account_invoice_view.xml", "data/email_templates.xml"],
    "installable": True,
}
