# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Stock Carrier Info",
    "version": "15.0.1.0.0",
    "category": "Stock",
    "license": "LGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "depends": ["delivery", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_carrier_info_views.xml",
        "views/stock_picking_view.xml",
    ],
    "installable": True,
}
