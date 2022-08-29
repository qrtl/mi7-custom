# Copyright 2021-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Validate Send Email",
    "category": "Accouting",
    "license": "AGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "version": "10.0.1.2.1",
    "depends": [
        "sale_stock",
        # "website_portal_sale",  # We may revive this when web_url is in use.
        "sale_automatic_workflow",
        "stock_picking_invoice_link",
        "stock_carrier_info",
    ],
    "data": [
        "data/email_templates.xml",
        "views/account_invoice_view.xml",
        "views/account_payment_term_views.xml",
        "views/sale_workflow_process_views.xml",
        "views/stock_carrier_info_views.xml",
        "views/stock_picking_views.xml",
        "views/res_company_views.xml",
    ],
    "installable": True,
}
