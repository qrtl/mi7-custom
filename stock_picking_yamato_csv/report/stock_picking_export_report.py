# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

# from odoo.exceptions import ValidationError

FIELDS_PROPERTIES = {
    # "shipping_mode": ["Char", 2],
    # "carrier_name": ["Char", 20],
    # "partner_ref": ["Char", 10],
    # "partner_zip": ["Char", 8],
    # "partner_address": ["Char", 80],
    # "product_code": ["Char", 7],
    # "product_name": ["Char", 32],
    # "case_qty": ["Float", 5],
    # "separate_qty": ["Float", 5],
    # "lot_num": ["Float", 6],
    # "lot_branch_num": ["Float", 2],
    # "delivery_division": ["Char", 1],
    # "customer_delivery_note": ["Char", 9],
    # "client_order_ref": ["Char", 30],
    # "memo": ["Char", 9],
}


class StockPickingExportReport(models.Model):
    _name = "stock.picking.export.report"

    move_id = fields.Many2one("stock.move", string="Stock Move", readonly=True)
    picking_id = fields.Many2one("stock.picking", string="Picking", readonly=True)
    comm_id = fields.Char("001 送信ID")
    request_categ = fields.Char("002 出荷指示処理区分")
    shipper_code = fields.Char("003 荷主コード")
    ship_categ = fields.Char("004 出荷種別区分")
    carrier_code = fields.Char("005 運送会社コード")
    dlv_fee_bill_to = fields.Char("006 運賃請求先顧客コード")
    dlv_fee_bill_to_br = fields.Char("007 運賃請求先顧客コード枝番")
    dlv_ctrl_number = fields.Char("008 運賃管理番号")
    whs_code = fields.Char("009 倉庫コード")
    dlv_rqstd_date = fields.Char("010 配送指定日")
    dlv_rqstd_date_categ = fields.Char("011 配送指定曜日区分")
    dlv_rqstd_time_categ = fields.Char("012 配送指定時間帯区分")
    dlv_service_categ = fields.Char("013 伝票区分")
    dlv_note_prnt_ctrl = fields.Char("014 納品書印字制御")
    gift_flag = fields.Char("015 ギフト判定フラグ")
    amount = fields.Integer("016 金額")
    b2_consump_amt = fields.Integer("017 B2連携用消費税額")
    pay_method_categ = fields.Char("018 支払方法区分")
    pay_div_number = fields.Char("019 分割回数")
    pay_div_amt = fields.Char("020 分割金額")
    adjust_amt = fields.Char("021 調整金額")
    amt1 = fields.Char("022 金額項目1")
    amt2 = fields.Char("023 金額項目2")
    amt3 = fields.Char("024 金額項目3")
    amt4 = fields.Char("025 金額項目4")
    amt5 = fields.Char("026 金額項目5")
    first_Pay_due = fields.Char("027 初回支払期限")
    dlv_fee = fields.Char("028 送料")
    num1 = fields.Char("029 数値項目1")
    num2 = fields.Char("030 数値項目2")
    num3 = fields.Char("031 数値項目3")
    num4 = fields.Char("032 数値項目4")
    num5 = fields.Char("033 数値項目5")
    partner_code = fields.Char("034 取引先コード")
    partner_name = fields.Char("035 取引先名称")
    partner_dept = fields.Char("036 取引先部署名")
    partner_contact = fields.Char("037 取引先担当者")
    partner_zip = fields.Char("038 取引先郵便番号")
    partner_address = fields.Char("039 取引先住所")
    partner_phone = fields.Char("040 取引先電話番号")
    partner_fax = fields.Char("041 取引先ＦＡＸ番号")
    partner_email = fields.Char("042 取引先メールアドレス")
    partner_email_type = fields.Char("043 取引先メール機種区分")
    ship_to_code = fields.Char("044 届先コード")
    ship_to_name = fields.Char("045 届先名称")
    ship_to_dept = fields.Char("046 届先部署名")
    ship_to_contact = fields.Char("047 届先担当者")
    ship_to_zip = fields.Char("048 届先郵便番号")
    ship_to_address = fields.Char("049 届先住所")
    ship_to_phone = fields.Char("050 届先電話番号")
    ship_to_fax = fields.Char("051 届先ＦＡＸ番号")
    scheduled_date = fields.Char("052 出荷予定日")
    request_date = fields.Char("053 出荷指示日")
    order_number = fields.Char("054 注文書番号")
    order_date = fields.Char("055 注文書日付")
    order_note = fields.Char("056 注文書注釈")
    origin_dept_code = fields.Char("057 発生元部署コード")
    origin_dept_signature = fields.Char("058 発生元部署名")
    origin_number = fields.Char("059 発生元番号")
    originated_date = fields.Char("060 発生日付")
    remark = fields.Char("061 備考")
    header_free01 = fields.Char("062 ヘッダーフリーエリア１")
    header_free02 = fields.Char("063 ヘッダーフリーエリア２")
    header_free03 = fields.Char("064 ヘッダーフリーエリア３")
    header_free04 = fields.Char("065 ヘッダーフリーエリア４")
    header_free05 = fields.Char("066 ヘッダーフリーエリア５")
    header_free06 = fields.Char("067 ヘッダーフリーエリア６")
    header_free07 = fields.Char("068 ヘッダーフリーエリア７")
    header_free08 = fields.Char("069 ヘッダーフリーエリア８")
    header_free09 = fields.Char("070 ヘッダーフリーエリア９")
    header_free10 = fields.Char("071 ヘッダーフリーエリア１０")
    dlv_note_field1 = fields.Char("072 納品書出力項目１")
    dlv_note_field2 = fields.Char("073 納品書出力項目２")
    dlv_note_field3 = fields.Char("074 納品書出力項目３")
    notif_email = fields.Char("075 出荷予定eメールアドレス")
    notif_email_type = fields.Char("076 入力機種種別")
    notif_email_message = fields.Char("077 出荷予定eメールメッセージ")
    pay_slip_categ = fields.Char("078 コンビニ区分")
    acquirer_name = fields.Char("079 事業者名")
    acquirer_zip = fields.Char("080 事業者郵便番号")
    acquirer_address1 = fields.Char("081 事業者住所１")
    acquirer_address2 = fields.Char("082 事業者住所２")
    first_invoice_message1 = fields.Char("083 初回請求メッセージ１")
    first_invoice_message2 = fields.Char("084 初回請求メッセージ２")
    invoice_number = fields.Char("085 請求No")
    ocr_info1 = fields.Char("086 OCR情報１行目")
    ocr_info2 = fields.Char("087 OCR情報２行目")
    barcode_info = fields.Char("088 バーコード情報")
    barcode_line1 = fields.Char("089 表示用バーコード1行目")
    barcode_line2 = fields.Char("090 表示用バーコード2行目")
    convn_due_date = fields.Char("091 コンビニ支払期限日")
    post_acct_agency_name = fields.Char("092 郵便口座所轄庁名")
    post_acct_agency_code = fields.Char("093 郵便口座所轄庁コード")
    post_check_digit = fields.Char("094 郵便チェックデジット")
    post_acct_number = fields.Char("095 郵便口座番号")
    private_apvl_number = fields.Char("096 私製承認番号")
    private_apvl_district = fields.Char("097 私製承認地区名")
    noshi_remark = fields.Char("098 熨斗表書き")
    noshi_wrap_categ = fields.Char("099 熨斗包装区分")
    noshi_paper_type = fields.Char("100 熨斗紙種類")
    noshi_name1 = fields.Char("101 名入れ１")
    noshi_name2 = fields.Char("102 名入れ２")
    noshi_name3 = fields.Char("103 名入れ３")
    allow_update = fields.Char("104 画面訂正可能フラグ")
    need_acceptance = fields.Char("105 納品書検品対象フラグ")
    request_item_categ = fields.Char("106 出荷指示明細処理区分")
    request_item_number = fields.Char("107 出荷指示明細番号")
    product_code = fields.Char("108 商品コード")
    packing_categ = fields.Char("109 荷姿区分")
    partner_product_code = fields.Char("110 取引先商品コード")
    location_code = fields.Char("111 ロケーションコード")
    state_code = fields.Char("112 状態コード")
    lot_number = fields.Char("113 ロット番号")
    serial_number = fields.Char("114 シリアル番号")
    expiration_date = fields.Char("115 賞味期限")
    inventory_categ_code = fields.Char("116 在庫切分けコード")
    ship_to_dsgnd_code = fields.Char("117 納品先指定コード")
    inventory_field1 = fields.Char("118 在庫管理項目１")
    inventory_field2 = fields.Char("119 在庫管理項目２")
    inventory_field3 = fields.Char("120 在庫管理項目３")
    inventory_field4 = fields.Char("121 在庫管理項目４")
    inventory_field5 = fields.Char("122 在庫管理項目５")
    inventory_field6 = fields.Char("123 在庫管理項目６")
    inventory_field7 = fields.Char("124 在庫管理項目７")
    inventory_date1 = fields.Char("125 在庫管理日付１")
    inventory_date2 = fields.Char("126 在庫管理日付２")
    inventory_date3 = fields.Char("127 在庫管理日付３")
    request_quantity = fields.Char("128 出荷指示数量")
    line_unit_price = fields.Char("129 本体金額(単価）")
    line_unit_tax = fields.Char("130 消費税金額")
    line_remark = fields.Char("131 備考")
    line_free01 = fields.Char("132 明細フリーエリア１")
    line_free02 = fields.Char("133 明細フリーエリア２")
    line_free03 = fields.Char("134 明細フリーエリア３")
    line_free04 = fields.Char("135 明細フリーエリア４")
    line_free05 = fields.Char("136 明細フリーエリア５")
    line_free06 = fields.Char("137 明細フリーエリア６")
    line_free07 = fields.Char("138 明細フリーエリア７")
    line_free08 = fields.Char("139 明細フリーエリア８")
    line_free09 = fields.Char("140 明細フリーエリア９")
    line_free10 = fields.Char("141 明細フリーエリア１０")
    is_exported = fields.Boolean("Exported")

    # @api.constrains(
    #     "shipping_mode",
    #     "carrier_name",
    #     "partner_ref",
    #     "partner_zip",
    #     "partner_address",
    #     "product_code",
    #     "product_name",
    #     "case_qty",
    #     "separate_qty",
    #     "lot_num",
    #     "lot_branch_num",
    #     "delivery_division",
    #     "customer_delivery_note",
    #     "client_order_ref",
    #     "memo",
    # )
    # def _validate_field_length(self):
    #     msg = _("%s should be at most %s digit(s).")
    #     for rec in self:
    #         for field, prop in FIELDS_PROPERTIES.items():
    #             if rec[field] and len(str(rec[field])) > prop[1]:
    #                 raise ValidationError(
    #                     msg % (_(rec.fields_get(field)[field].get("string")), prop[1])
    #                 )

    # @api.constrains("case_qty", "separate_qty", "lot_num", "lot_branch_num")
    # def _validate_number_fields(self):
    #     msg = _("Only numbers are allowed for %s field.")
    #     for rec in self:
    #         for field, prop in FIELDS_PROPERTIES.items():
    #             if prop[0] == "Float":
    #                 try:
    #                     int(rec[field])
    #                 except Exception:
    #                     try:
    #                         float(rec[field])
    #                     except Exception:
    #                         raise ValidationError(
    #                             msg % _(rec.fields_get(field)[field].get("string"))
    #                         )

    # _sql_constraints = [
    #     ("move_id_uniq", "unique(move_id)", "The stock data already exists.")
    # ]
