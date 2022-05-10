# -*- coding: utf-8 -*-
# Copyright 2021-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Yamato CSV",
    "version": "10.0.1.1.3",
    "category": "Stock",
    "website": "https://www.quartile.co/",
    "author": "Quartile Limited",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale_stock",
        "company_alternative_attribute",  # alt_name (res.company)
        "report_csv",
        "sale_customer_order_info",  # customer_order, customer_contact
        "sale_user_type",  # For user_type
        "stock_product_availability",  # person (sale.order)
        "website_sale_delivery_date",  # For delivery_date, delivery_time_id
    ],
    "data": [
        "views/res_partner_views.xml",
        "views/shipping_timerange_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_warehouse_views.xml",
    ],
}
