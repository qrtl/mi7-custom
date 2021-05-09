# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Stock Picking Import Validate",
    "version": "10.0.1.0.0",
    "category": "Stock",
    "license": "LGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co/",
    "depends": ["stock", "base_import_log", "queue_job"],
    "data": [
        "views/error_log_views.xml",
        "wizard/stock_picking_import_views.xml",
    ],
    "installable": True,
}
