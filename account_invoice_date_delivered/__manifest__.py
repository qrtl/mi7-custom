# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Date Delivered",
    "category": "Accouting",
    "license": "AGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "version": "15.0.1.0.0",
    "depends": ["base_timezone_converter", "stock_picking_invoice_link"],
    "data": ["views/account_move_views.xml"],
    "pre_init_hook": "pre_init_hook",
    "installable": True,
}
