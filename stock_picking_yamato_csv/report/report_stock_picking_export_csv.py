# -*- coding: utf-8 -*-
# Copyright 2020 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv

from odoo import _, models


class StockPickingExportCSV(models.AbstractModel):
    _name = "report.report_csv.stock_picking_export_csv"
    _inherit = "report.report_csv.abstract"

    def _encode_sjis(self, val):
        if val:
            if isinstance(val, unicode):
                val = val.encode("cp932")
            elif isinstance(val, str):
                val = unicode(val).encode("cp932")
        return val

    def _get_fields(self):
        fields = {
            1: _("出荷指示処理区分"),
            2: _("荷主コード"),
            3: _("出荷種別区分"),
            4: _("運送会社コード"),
        }
        fields = {k: self._encode_sjis(v) for k, v in fields.items()}
        return fields
    
    def generate_csv_report(self, writer, data, export_report):
        writer.writeheader()
        fields = self._get_fields()
        for rec in export_report:
            writer.writerow({
                fields[1]: rec.request_categ,
                fields[2]: rec.shipper_code,
                fields[3]: rec.ship_categ,
            })
            rec.is_exported = True

    def csv_report_options(self):
        res = super(StockPickingExportCSV, self).csv_report_options()
        fields = self._get_fields()
        for k, v in fields.items():
            res["fieldnames"].append(v)
        res['delimiter'] = ','
        res['quoting'] = csv.QUOTE_MINIMAL
        return res

    # def generate_csv_report(self, data, orders, file_data):
    #     writer = csv.DictWriter(
    #         file_data, **self.csv_report_options(), quoting=csv.QUOTE_NONE
    #     )
    #     writer.writeheader()
    #     writer = csv.DictWriter(
    #         file_data, **self.csv_report_options(), quoting=csv.QUOTE_ALL
    #     )
    #     for order in orders:
    #         shipping_cost = sum(
    #             [line.price_subtotal for line in order.order_line if line.is_delivery]
    #         )
    #         writer.writerow(
    #             {
    #                 "Order ID": order.rakushisu_order_id,
    #                 "E-mail": order.partner_id.email,
    #                 "User ID": order.partner_id.tecro_user_id or "",
    #                 "Total": order.amount_untaxed,
    #                 "Subtotal": order.amount_untaxed - shipping_cost,
    #                 "Discount": 0,
    #                 "Payment surcharge": 0,
    #                 "Shipping cost": shipping_cost,
    #                 "Date": order.confirmation_date
    #                 and order.confirmation_date.strftime("%d %b %Y %H:%M:%S")
    #                 or "",
    #                 "Status": order.rakushisu_status
    #                 or self.env["ir.config_parameter"]
    #                 .sudo()
    #                 .get_param("sale_order_export_rpl.rakushisu_status", default=""),
    #                 "Notes": order.note,
    #                 "Payment ID": self.env["ir.config_parameter"]
    #                 .sudo()
    #                 .get_param(
    #                     "sale_order_export_rpl.rakushisu_payment_id", default=12
    #                 ),
    #                 "IP address": self.env["ir.config_parameter"]
    #                 .sudo()
    #                 .get_param(
    #                     "sale_order_export_rpl.rakushisu_ip_address", default=""
    #                 ),
    #                 "Details": order.note2
    #                 and html2text.html2text(order.note2).replace("\n", " ")
    #                 or "",
    #                 "Payment information": "",
    #                 "Taxes": "",
    #                 "Coupons": "",
    #                 "Shipping": "",
    #                 # 担当者情報　要確認
    #                 "Title": "",
    #                 "First name": "",
    #                 "Last name": "",
    #                 "Company": order.partner_id.commercial_partner_id.name,
    #                 "Fax": "",
    #                 "Phone": order.partner_shipping_id.phone,
    #                 "Web site": "",
    #                 "Tax exempt": "N",
    #                 "Language": self.env["ir.config_parameter"]
    #                 .sudo()
    #                 .get_param("sale_order_export_rpl.rakushisu_language", default=""),
    #                 # 請求先情報
    #                 "Billing: title": order.partner_invoice_id.title
    #                 and order.partner_invoice_id.title.name
    #                 or "",
    #                 "Billing: first name": order.partner_invoice_id.name,
    #                 "Billing: last name": "",  # 要確認
    #                 "Billing: address": order.partner_invoice_id.street or "",
    #                 "Billing: address (line 2)": order.partner_invoice_id.street2 or "",
    #                 "Billing: city": order.partner_invoice_id.city or "",
    #                 "Billing: state": order.partner_invoice_id.state_id
    #                 and order.partner_invoice_id.state_id.code
    #                 or "",
    #                 "Billing: country": order.partner_invoice_id.country_id
    #                 and order.partner_invoice_id.country_id.code
    #                 or "",
    #                 "Billing: zipcode": order.partner_invoice_id.zip,
    #                 "Shipping: title": order.partner_shipping_id.title
    #                 and order.partner_shipping_id.title.name
    #                 or "",
    #                 # 配送先情報
    #                 "Shipping: first name": order.partner_shipping_id.name,
    #                 "Shipping: last name": "",  # 要確認
    #                 "Shipping: address": order.partner_shipping_id.street or "",
    #                 "Shipping: address (line 2)": order.partner_shipping_id.street2
    #                 or "",
    #                 "Shipping: city": order.partner_shipping_id.city or "",
    #                 "Shipping: state": order.partner_shipping_id.state_id
    #                 and order.partner_shipping_id.state_id.code
    #                 or "",
    #                 "Shipping: country": order.partner_shipping_id.country_id
    #                 and order.partner_shipping_id.country_id.code
    #                 or "",
    #                 "Shipping: zipcode": order.partner_invoice_id.zip,
    #                 "Invoice ID": "",
    #                 "Credit memo ID": "",
    #                 "payment_date": "",  # 要確認
    #             }
    #         )

    # def csv_report_options(self):
    #     res = super().csv_report_options()
    #     res["fieldnames"].append("Order ID")
    #     res["fieldnames"].append("E-mail")
    #     res["fieldnames"].append("User ID")
    #     res["fieldnames"].append("Total")
    #     res["fieldnames"].append("Subtotal")
    #     res["fieldnames"].append("Discount")
    #     res["fieldnames"].append("Payment surcharge")
    #     res["fieldnames"].append("Shipping cost")
    #     res["fieldnames"].append("Date")
    #     res["fieldnames"].append("Status")
    #     res["fieldnames"].append("Notes")
    #     res["fieldnames"].append("Payment ID")
    #     res["fieldnames"].append("IP address")
    #     res["fieldnames"].append("Details")
    #     res["fieldnames"].append("Payment information")
    #     res["fieldnames"].append("Taxes")
    #     res["fieldnames"].append("Coupons")
    #     res["fieldnames"].append("Shipping")
    #     res["fieldnames"].append("Title")
    #     res["fieldnames"].append("First name")
    #     res["fieldnames"].append("Last name")
    #     res["fieldnames"].append("Company")
    #     res["fieldnames"].append("Fax")
    #     res["fieldnames"].append("Phone")
    #     res["fieldnames"].append("Web site")
    #     res["fieldnames"].append("Tax exempt")
    #     res["fieldnames"].append("Language")
    #     res["fieldnames"].append("Billing: title")
    #     res["fieldnames"].append("Billing: first name")
    #     res["fieldnames"].append("Billing: last name")
    #     res["fieldnames"].append("Billing: address")
    #     res["fieldnames"].append("Billing: address (line 2)")
    #     res["fieldnames"].append("Billing: city")
    #     res["fieldnames"].append("Billing: state")
    #     res["fieldnames"].append("Billing: country")
    #     res["fieldnames"].append("Billing: zipcode")
    #     res["fieldnames"].append("Shipping: title")
    #     res["fieldnames"].append("Shipping: first name")
    #     res["fieldnames"].append("Shipping: last name")
    #     res["fieldnames"].append("Shipping: address")
    #     res["fieldnames"].append("Shipping: address (line 2)")
    #     res["fieldnames"].append("Shipping: city")
    #     res["fieldnames"].append("Shipping: state")
    #     res["fieldnames"].append("Shipping: country")
    #     res["fieldnames"].append("Shipping: zipcode")
    #     res["fieldnames"].append("Invoice ID")
    #     res["fieldnames"].append("Credit memo ID")
    #     res["fieldnames"].append("payment_date")
    #     res["delimiter"] = ","
    #     res["lineterminator"] = "\n"
    #     return res
