# -*- coding: utf-8 -*-
# Copyright 2021-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv
from datetime import datetime

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class StockPickingYamatoCSV(models.AbstractModel):
    _name = "report.stock_picking_yamato_csv.report_yamato_csv"
    _inherit = "report.report_csv.abstract"

    def _get_field_dict(self):
        field_dict = {
            1: _("送信ID"),
            2: _("出荷指示処理区分"),
            3: _("荷主コード"),
            4: _("出荷種別区分"),
            5: _("運送会社コード"),
            6: _("運賃請求先顧客コード"),
            7: _("運賃請求先顧客コード枝番"),
            8: _("運賃管理番号"),
            9: _("倉庫コード"),
            10: _("配送指定日"),
            11: _("配送指定曜日区分"),
            12: _("配送指定時間帯区分"),
            13: _("伝票区分"),
            14: _("納品書印字制御"),
            15: _("ギフト判定フラグ"),
            16: _("金額"),
            17: _("B2連携用消費税額"),
            18: _("支払方法区分"),
            19: _("分割回数"),
            20: _("分割金額"),
            21: _("調整金額"),
            22: _("金額項目1"),
            23: _("金額項目2"),
            24: _("金額項目3"),
            25: _("金額項目4"),
            26: _("金額項目5"),
            27: _("初回支払期限"),
            28: _("送料"),
            29: _("数値項目1"),
            30: _("数値項目2"),
            31: _("数値項目3"),
            32: _("数値項目4"),
            33: _("数値項目5"),
            34: _("取引先コード"),
            35: _("取引先名称"),
            36: _("取引先部署名"),
            37: _("取引先担当者"),
            38: _("取引先郵便番号"),
            39: _("取引先住所"),
            40: _("取引先電話番号"),
            41: _("取引先ＦＡＸ番号"),
            42: _("取引先メールアドレス"),
            43: _("取引先メール機種区分"),
            44: _("届先コード"),
            45: _("届先名称"),
            46: _("届先部署名"),
            47: _("届先担当者"),
            48: _("届先郵便番号"),
            49: _("届先住所"),
            50: _("届先電話番号"),
            51: _("届先ＦＡＸ番号"),
            52: _("出荷予定日"),
            53: _("出荷指示日"),
            54: _("注文書番号"),
            55: _("注文書日付"),
            56: _("注文書注釈"),
            57: _("発生元部署コード"),
            58: _("発生元部署名"),
            59: _("発生元番号"),
            60: _("発生日付"),
            61: _("備考"),
            62: _("ヘッダーフリーエリア１"),
            63: _("ヘッダーフリーエリア２"),
            64: _("ヘッダーフリーエリア３"),
            65: _("ヘッダーフリーエリア４"),
            66: _("ヘッダーフリーエリア５"),
            67: _("ヘッダーフリーエリア６"),
            68: _("ヘッダーフリーエリア７"),
            69: _("ヘッダーフリーエリア８"),
            70: _("ヘッダーフリーエリア９"),
            71: _("ヘッダーフリーエリア１０"),
            72: _("納品書出力項目１"),
            73: _("納品書出力項目２"),
            74: _("納品書出力項目３"),
            75: _("出荷予定eメールアドレス"),
            76: _("入力機種種別"),
            77: _("出荷予定eメールメッセージ"),
            78: _("コンビニ区分"),
            79: _("事業者名"),
            80: _("事業者郵便番号"),
            81: _("事業者住所１"),
            82: _("事業者住所２"),
            83: _("初回請求メッセージ１"),
            84: _("初回請求メッセージ２"),
            85: _("請求No"),
            86: _("OCR情報１行目"),
            87: _("OCR情報２行目"),
            88: _("バーコード情報"),
            89: _("表示用バーコード1行目"),
            90: _("表示用バーコード2行目"),
            91: _("コンビニ支払期限日"),
            92: _("郵便口座所轄庁名"),
            93: _("郵便口座所轄庁コード"),
            94: _("郵便チェックデジット"),
            95: _("郵便口座番号"),
            96: _("私製承認番号"),
            97: _("私製承認地区名"),
            98: _("熨斗表書き"),
            99: _("熨斗包装区分"),
            100: _("熨斗紙種類"),
            101: _("名入れ１"),
            102: _("名入れ２"),
            103: _("名入れ３"),
            104: _("画面訂正可能フラグ"),
            105: _("納品書検品対象フラグ"),
            106: _("出荷指示明細処理区分"),
            107: _("出荷指示明細番号"),
            108: _("商品コード"),
            109: _("荷姿区分"),
            110: _("取引先商品コード"),
            111: _("ロケーションコード"),
            112: _("状態コード"),
            113: _("ロット番号"),
            114: _("シリアル番号"),
            115: _("賞味期限"),
            116: _("在庫切分けコード"),
            117: _("納品先指定コード"),
            118: _("在庫管理項目１"),
            119: _("在庫管理項目２"),
            120: _("在庫管理項目３"),
            121: _("在庫管理項目４"),
            122: _("在庫管理項目５"),
            123: _("在庫管理項目６"),
            124: _("在庫管理項目７"),
            125: _("在庫管理日付１"),
            126: _("在庫管理日付２"),
            127: _("在庫管理日付３"),
            128: _("出荷指示数量"),
            129: _("本体金額(単価）"),
            130: _("消費税金額"),
            131: _("備考"),
            132: _("明細フリーエリア１"),
            133: _("明細フリーエリア２"),
            134: _("明細フリーエリア３"),
            135: _("明細フリーエリア４"),
            136: _("明細フリーエリア５"),
            137: _("明細フリーエリア６"),
            138: _("明細フリーエリア７"),
            139: _("明細フリーエリア８"),
            140: _("明細フリーエリア９"),
            141: _("明細フリーエリア１０"),
        }
        field_dict = {k: self._encode_sjis(v) for k, v in field_dict.items()}
        return field_dict

    def _get_address(self, partner):
        address = ""
        if partner.state_id:
            address += partner.state_id.name
        if partner.city:
            address += partner.city
        if partner.street:
            address += partner.street
        if partner.street2:
            address += " " + partner.street2
        return address

    def _get_sender_name(self, order, company, whs_partner):
        if order.user_type == "b2c":
            return company.alt_name
        return whs_partner.name if whs_partner else company.name

    def _encode_sjis(self, val):
        if val:
            if isinstance(val, unicode):  # noqa
                val = val.encode("cp932")
            elif isinstance(val, str):
                val = unicode(val).encode("cp932")  # noqa
        return val

    def _get_date(self, dt_date):
        """This method converts datetime to date in user's timezone.
        """
        return fields.Datetime.context_timestamp(
            self, fields.Datetime.from_string(dt_date)
        ).strftime("%Y%m%d")

    def _check_pickings(self, pickings):
        invalid_picks = pickings.filtered(
            lambda x: x.state in ("draft", "cancel", "done")
        )
        if invalid_picks:
            raise UserError(
                _(
                    "Following records are in invalid state (draft/done/cancel) for an export.\n%s"
                )
                % ("\n".join(invalid_picks.mapped("name")))
            )
        exported_picks = pickings.filtered(lambda x: x.is_exported)
        if exported_picks:
            raise UserError(
                _(
                    "Following records have been exported already. Please "
                    "unselect 'Exported' as necessary to export them again.\n%s"
                )
                % ("\n".join(exported_picks.mapped("name")))
            )
        no_order_picks = pickings.filtered(lambda x: not x.sale_id)
        if no_order_picks:
            raise UserError(
                _("Following records have no sales orders linked to them.\n%s")
                % ("\n".join(no_order_picks.mapped("name")))
            )
        no_partner_picks = pickings.filtered(lambda x: not x.partner_id)
        if no_partner_picks:
            raise UserError(
                _("Following records have no partners linked to them.\n%s")
                % ("\n".join(no_partner_picks.mapped("name")))
            )

    def _get_amounts(self, picking):
        amt_taxinc = amt_tax = 0.0
        for move in picking.move_lines:
            sale_line = move.procurement_id.sale_line_id
            amt_taxinc += move.product_uom_qty * sale_line.price_reduce_taxinc
            amt_tax += move.product_uom_qty * (
                sale_line.price_reduce_taxinc - sale_line.price_reduce_taxexcl
            )
        for sale_line in picking.sale_id.order_line:
            # For cash-on-delivery and delivery fees. We assume that there will
            # be no multiple deliveries for an order involving COD.
            if sale_line.product_id.default_code == "COD" or sale_line.is_delivery:
                amt_taxinc += sale_line.product_uom_qty * sale_line.price_reduce_taxinc
                amt_tax += sale_line.product_uom_qty * (
                    sale_line.price_reduce_taxinc - sale_line.price_reduce_taxexcl
                )
        return amt_taxinc, amt_tax

    def generate_csv_report(self, writer, data, pickings):
        self._check_pickings(pickings)
        today_date = self._get_date(fields.Datetime.now())
        writer.writeheader()
        field_dict = self._get_field_dict()
        item_num = 1
        for picking in pickings:
            warehouse = picking.picking_type_id.warehouse_id
            whs_partner = warehouse.partner_id
            company = picking.company_id
            order = picking.sale_id
            pick_create_date = self._get_date(picking.date)
            scheduled_date = self._get_date(picking.min_date)
            partner_shipping = picking.partner_id
            carrier_code = (
                picking.yamato_carrier_code
                or partner_shipping.yamato_carrier_code
                or warehouse.yamato_carrier_code
            )
            if scheduled_date < today_date:
                raise UserError(
                    _("There is a delivery with a past scheduled date: %s")
                    % (picking.name)
                )
            # 伝票区分 '00' means that 送り状 will not be issued.
            slip_categ = "00"
            if carrier_code != "ZZZ01":
                slip_categ = "20" if order.is_cod else "10"
            amt_taxinc, amt_tax = self._get_amounts(picking)
            for move in picking.move_lines:
                vals = {
                    field_dict[2]: "1",  # Newly create
                    field_dict[3]: warehouse.yamato_shipper_code,
                    field_dict[4]: "10",
                    field_dict[5]: carrier_code,
                    field_dict[9]: "S001",
                    field_dict[10]: order.delivery_date
                    and datetime.strptime(
                        order.delivery_date, DEFAULT_SERVER_DATE_FORMAT
                    ).strftime("%Y%m%d")
                    or "",
                    field_dict[12]: order.delivery_time_id
                    and order.delivery_time_id.delivery_time_categ
                    or "",
                    field_dict[13]: slip_categ,
                    field_dict[16]: int(amt_taxinc),
                    field_dict[17]: int(amt_tax),
                    field_dict[35]: self._encode_sjis(
                        self._get_sender_name(order, company, whs_partner)
                    ),
                    field_dict[38]: whs_partner.zip if whs_partner else company.zip,
                    field_dict[39]: self._encode_sjis(
                        self._get_address(whs_partner or company)
                    ),
                    field_dict[40]: whs_partner.phone if whs_partner else company.phone,
                    field_dict[45]: self._encode_sjis(partner_shipping.name),
                    field_dict[47]: self._encode_sjis(order.person) or "",
                    field_dict[48]: partner_shipping.zip,
                    field_dict[49]: self._encode_sjis(
                        self._get_address(partner_shipping)
                    ),
                    field_dict[50]: partner_shipping.phone,
                    field_dict[52]: scheduled_date,
                    field_dict[53]: today_date,
                    field_dict[54]: picking.name,
                    field_dict[59]: picking.name,
                    field_dict[60]: pick_create_date,
                    field_dict[61]: self._encode_sjis(order.customer_order) or "",
                    field_dict[72]: self._encode_sjis(order.customer_order) or "",
                    field_dict[104]: "1",  # Allow edit on screen
                    field_dict[105]: "0",
                    field_dict[106]: "1",  # Mewly create
                    field_dict[107]: item_num,
                    field_dict[108]: move.product_id.default_code,
                    field_dict[109]: "00",  # Fixed as 'bara'
                    field_dict[128]: int(move.product_uom_qty),
                }
                writer.writerow(vals)
                item_num += 1
            picking.is_exported = True

    def csv_report_options(self):
        res = super(StockPickingYamatoCSV, self).csv_report_options()
        field_dict = self._get_field_dict()
        for k, v in field_dict.items():
            res["fieldnames"].append(v)
        res["delimiter"] = ","
        res["quoting"] = csv.QUOTE_MINIMAL
        return res
