# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Sale Delivery Date",
    "category": "Sale",
    "version": "15.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "base_timezone_converter",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_config_parameter.xml",
        "views/sale_order_views.xml",
        "views/shipping_timerange_ec_views.xml",
    ],
    "installable": True,
}
