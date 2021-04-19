# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Stock Picking Export Report",
    "version": "10.0.1.0.0",
    "category": "Stock",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["sale_stock", "pro_mi7_website_sale_ec", "report_csv"],
    "data": [
        "security/ir.model.access.csv",
        "data/stock_picking_export_report_data.xml",
        "report/stock_picking_export_report.xml",
        "views/res_company_views.xml",
        "views/shipping_timerange_views.xml",
        "views/stock_picking_export_report_views.xml",
        "views/stock_picking_views.xml",
    ],
}
