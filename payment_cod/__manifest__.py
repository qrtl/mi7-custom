# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Payment Cash on Delivery",
    "category": "Website",
    "version": "15.0.1.0.0",
    "author": "MI Seven Japan, Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "depends": ["payment_transfer", "sale"],
    "data": [
        "data/payment_acquirer_data.xml",
        "views/payment_acquirer_views.xml",
        "views/templates.xml",
    ],
    "installable": True,
}
