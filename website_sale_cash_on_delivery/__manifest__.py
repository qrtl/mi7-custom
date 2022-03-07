# -*- coding: utf-8 -*-
# Copyright 2018-2021 MI Seven Japan
# Copyright 2022 Quartile Limited
{
    "name": "Website Sale Cash on Delivery",
    "category": "Website",
    "version": "10.0.1.0.0",
    "author": "MI Seven Japan, Quartile Limited",
    "license": "Other proprietary",
    "depends": [
        "sale_physical_product",  # For is_physical (product.template)
        "website_sale",
    ],
    "data": ["views/payment_acquirer_views.xml", "views/templates.xml",],
    "installable": True,
}
