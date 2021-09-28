# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Stock Delivery Result Import",
    "version": "10.0.1.1.0",
    "category": "Stock",
    "license": "LGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co/",
    "depends": ["stock", "base_data_import", "queue_job", "stock_carrier_info"],
    "data": [
        "views/data_import_log_views.xml",
        "wizards/stock_delivery_result_import_views.xml",
    ],
    "installable": True,
}
