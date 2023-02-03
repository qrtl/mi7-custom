# Copyright 2021-2022 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import codecs
import csv

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPickingYamatoCSV(models.AbstractModel):
    _name = "report.stock_picking_yamato_csv.report_yamato_csv"
    _inherit = "report.report_csv.abstract"

    def _get_field_dict(self):
        field_dict = {
            1: "送信ID",
            2: "出荷指示処理区分",
            3: "荷主コード",
            4: "出荷種別区分",
            5: "運送会社コード",
            6: "運賃請求先顧客コード",
            7: "運賃請求先顧客コード枝番",
            8: "運賃管理番号",
            9: "倉庫コード",
            10: "配送指定日",
            11: "配送指定曜日区分",
            12: "配送指定時間帯区分",
            13: "伝票区分",
            14: "納品書印字制御",
            15: "ギフト判定フラグ",
            16: "金額",
            17: "B2連携用消費税額",
            18: "支払方法区分",
            19: "分割回数",
            20: "分割金額",
            21: "調整金額",
            22: "金額項目1",
            23: "金額項目2",
            24: "金額項目3",
            25: "金額項目4",
            26: "金額項目5",
            27: "初回支払期限",
            28: "送料",
            29: "数値項目1",
            30: "数値項目2",
            31: "数値項目3",
            32: "数値項目4",
            33: "数値項目5",
            34: "取引先コード",
            35: "取引先名称",
            36: "取引先部署名",
            37: "取引先担当者",
            38: "取引先郵便番号",
            39: "取引先住所",
            40: "取引先電話番号",
            41: "取引先ＦＡＸ番号",
            42: "取引先メールアドレス",
            43: "取引先メール機種区分",
            44: "届先コード",
            45: "届先名称",
            46: "届先部署名",
            47: "届先担当者",
            48: "届先郵便番号",
            49: "届先住所",
            50: "届先電話番号",
            51: "届先ＦＡＸ番号",
            52: "出荷予定日",
            53: "出荷指示日",
            54: "注文書番号",
            55: "注文書日付",
            56: "注文書注釈",
            57: "発生元部署コード",
            58: "発生元部署名",
            59: "発生元番号",
            60: "発生日付",
            61: "備考",
            62: "ヘッダーフリーエリア１",
            63: "ヘッダーフリーエリア２",
            64: "ヘッダーフリーエリア３",
            65: "ヘッダーフリーエリア４",
            66: "ヘッダーフリーエリア５",
            67: "ヘッダーフリーエリア６",
            68: "ヘッダーフリーエリア７",
            69: "ヘッダーフリーエリア８",
            70: "ヘッダーフリーエリア９",
            71: "ヘッダーフリーエリア１０",
            72: "納品書出力項目１",
            73: "納品書出力項目２",
            74: "納品書出力項目３",
            75: "出荷予定eメールアドレス",
            76: "入力機種種別",
            77: "出荷予定eメールメッセージ",
            78: "コンビニ区分",
            79: "事業者名",
            80: "事業者郵便番号",
            81: "事業者住所１",
            82: "事業者住所２",
            83: "初回請求メッセージ１",
            84: "初回請求メッセージ２",
            85: "請求No",
            86: "OCR情報１行目",
            87: "OCR情報２行目",
            88: "バーコード情報",
            89: "表示用バーコード1行目",
            90: "表示用バーコード2行目",
            91: "コンビニ支払期限日",
            92: "郵便口座所轄庁名",
            93: "郵便口座所轄庁コード",
            94: "郵便チェックデジット",
            95: "郵便口座番号",
            96: "私製承認番号",
            97: "私製承認地区名",
            98: "熨斗表書き",
            99: "熨斗包装区分",
            100: "熨斗紙種類",
            101: "名入れ１",
            102: "名入れ２",
            103: "名入れ３",
            104: "画面訂正可能フラグ",
            105: "納品書検品対象フラグ",
            106: "出荷指示明細処理区分",
            107: "出荷指示明細番号",
            108: "商品コード",
            109: "荷姿区分",
            110: "取引先商品コード",
            111: "ロケーションコード",
            112: "状態コード",
            113: "ロット番号",
            114: "シリアル番号",
            115: "賞味期限",
            116: "在庫切分けコード",
            117: "納品先指定コード",
            118: "在庫管理項目１",
            119: "在庫管理項目２",
            120: "在庫管理項目３",
            121: "在庫管理項目４",
            122: "在庫管理項目５",
            123: "在庫管理項目６",
            124: "在庫管理項目７",
            125: "在庫管理日付１",
            126: "在庫管理日付２",
            127: "在庫管理日付３",
            128: "出荷指示数量",
            129: "本体金額(単価）",
            130: "消費税金額",
            131: "備考",
            132: "明細フリーエリア１",
            133: "明細フリーエリア２",
            134: "明細フリーエリア３",
            135: "明細フリーエリア４",
            136: "明細フリーエリア５",
            137: "明細フリーエリア６",
            138: "明細フリーエリア７",
            139: "明細フリーエリア８",
            140: "明細フリーエリア９",
            141: "明細フリーエリア１０",
        }
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

    @api.model
    def _get_website_name(self, order, company):
        if order.website_id:
            return order.website_id.name
        website = self.env["website"].search([("company_id", "=", company.id)], limit=1)
        if website:
            return website.name
        return False

    def _get_sender_name(self, order, company, whs_partner):
        if order.user_type == "b2c":
            return self._get_website_name(order, company)
        return whs_partner.name if whs_partner else company.name

    def _get_date(self, dt_date):
        """This method converts datetime to date in user's timezone."""
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
                    "Following records are in invalid state (draft/done/cancel) for an "
                    "export.\n%s"
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
            sale_line = move.sale_line_id
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

    @api.model
    def is_encodable(self, key, value):
        try:
            codecs.encode(value, "cp932")
        except UnicodeEncodeError as e:
            raise UserError(
                _("Failed to encode the value of the following field: %s") % (key)
            ) from e

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
            scheduled_date = self._get_date(picking.scheduled_date)
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
                    and order.delivery_date.strftime("%Y%m%d")
                    or "",
                    field_dict[12]: order.delivery_time_id
                    and order.delivery_time_id.delivery_time_categ
                    or "",
                    field_dict[13]: slip_categ,
                    field_dict[16]: int(amt_taxinc),
                    field_dict[17]: int(amt_tax),
                    field_dict[35]: self._get_sender_name(order, company, whs_partner),
                    field_dict[38]: whs_partner.zip if whs_partner else company.zip,
                    field_dict[39]: self._get_address(whs_partner or company),
                    field_dict[40]: whs_partner.phone if whs_partner else company.phone,
                    field_dict[45]: partner_shipping.name,
                    field_dict[47]: order.customer_contact or "",
                    field_dict[48]: partner_shipping.zip,
                    field_dict[49]: self._get_address(partner_shipping),
                    field_dict[50]: partner_shipping.phone,
                    field_dict[52]: scheduled_date,
                    field_dict[53]: today_date,
                    field_dict[54]: picking.name,
                    field_dict[59]: picking.name,
                    field_dict[60]: pick_create_date,
                    field_dict[61]: order.customer_order or "",
                    field_dict[72]: order.customer_order or "",
                    field_dict[104]: "1",  # Allow edit on screen
                    field_dict[105]: "0",
                    field_dict[106]: "1",  # Mewly create
                    field_dict[107]: item_num,
                    field_dict[108]: move.product_id.default_code,
                    field_dict[109]: "00",  # Fixed as 'bara'
                    field_dict[128]: int(move.product_uom_qty),
                }
                writer.writerow(vals)
                for k, v in vals.items():
                    self.is_encodable(k, v)
                item_num += 1
            picking.is_exported = True

    def csv_report_options(self):
        res = super(StockPickingYamatoCSV, self).csv_report_options()
        field_dict = self._get_field_dict()
        for _k, v in field_dict.items():
            res["fieldnames"].append(v)
        res["delimiter"] = ","
        res["quoting"] = csv.QUOTE_MINIMAL
        return res
