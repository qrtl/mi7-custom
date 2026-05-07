# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Product Tag",
    "category": "Product",
    "version": "15.0.1.0.0",
    "author": "Quartile",
    "website": "https://www.quartile.co",
    "license": "LGPL-3",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_tag_views.xml",
        "views/product_template_views.xml",
        "views/product_views.xml",
    ],
    "installable": True,
}
