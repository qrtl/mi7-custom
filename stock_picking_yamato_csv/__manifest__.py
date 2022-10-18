# Copyright 2021-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Yamato CSV",
    "version": "15.0.1.0.0",
    "category": "Stock",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
        "report_csv",
        "sale_customer_order_info",  # customer_order, customer_contact
        "sale_user_type",  # For user_type
        "sale_delivery_date",  # For delivery_date, delivery_time_id
    ],
    "data": [
        "data/yamato_csv_report_data.xml",
        "views/res_partner_views.xml",
        "views/shipping_timerange_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_warehouse_views.xml",
    ],
    "installable": True,
}
