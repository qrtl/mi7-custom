# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Stock Outgoing Shipment Report",
    "summary": "",
    "version": "10.0.1.0.0",
    "category": "Stock",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["sale_stock"],
    "data": [
        "security/ir.model.access.csv",
        "data/stock_outgoing_shipment_report_data.xml",
        "views/stock_outgoing_shipment_report_views.xml",
        "views/stock_picking_views.xml",
    ],
}
