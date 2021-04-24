# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Yamato CSV",
    "version": "10.0.1.0.0",
    "category": "Stock",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["sale_stock", "pro_mi7_sale", "pro_mi7_website_sale_ec", "report_csv"],
    "data": [
        # "security/ir.model.access.csv",
        # "data/stock_picking_export_report_data.xml",
        # "data/stock_picking_yamato_csv_report.xml",
        "views/res_company_views.xml",
        "views/shipping_timerange_views.xml",
        # "views/stock_picking_export_report_views.xml",
        "views/stock_picking_views.xml",
    ],
}
