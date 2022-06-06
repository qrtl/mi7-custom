# -*- coding: utf-8 -*-
# Copyright 2022 Quartile Limited
{
    "name": "Website Sale Product Check",
    "category": "Website",
    "version": "10.0.1.0.0",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "Other proprietary",  # TODO: switch to LGPL when possible
    "depends": [
        "website_sale",
        "clarico_product",  # TODO: remove this dependency
    ],
    "data": ["views/templates.xml"],
    "installable": True,
}
