# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Validate Send Email",
    "category": "Accouting",
    "license": "AGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "version": "10.0.1.0.1",
    "depends": [
        "pro_mi7_account",
        "sale_automatic_workflow",
        "stock_picking_invoice_link",
        "website_portal_sale",
    ],
    "data": [
        "data/email_templates.xml",
        "views/account_invoice_view.xml",
        "views/account_payment_term_views.xml",
        "views/sale_workflow_process_views.xml",
        "views/stock_picking_views.xml",
        "views/res_company_views.xml",
    ],
    "installable": True,
}
