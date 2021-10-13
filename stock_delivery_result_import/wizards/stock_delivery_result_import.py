# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, models

FIELD_KEYS = {0: "field", 1: "label", 2: "field_type", 3: "required"}
# Prepare values corresponding with the keys
FIELD_VALS = [
    ["picking_ref", "受注番号", "char", True],
    ["carrier_code", "運送会社コード", "char", False],
    ["tracking_ref", "伝票番号", "char", False],
]


class StockDeliveryResultImport(models.TransientModel):
    _name = "stock.delivery.result.import"
    _inherit = "data.import"

    @api.model
    def _update_pick_dict_carrier_info(
        self, carrier_code, error_list, pick_dict, picking
    ):
        carrier_info = self.env["stock.carrier.info"].search(
            [("code", "=", carrier_code)]
        )[:1]
        if carrier_info:
            if picking.carrier_info_id:
                if picking.carrier_info_id != carrier_info:
                    error_list.append(
                        _(
                            "Warehouse Carrier is inconsistent between the current "
                            "setting and the imported data."
                        )
                    )
            else:
                pick_dict[picking]["carrier_info"] = carrier_info
        else:
            error_list.append(
                _("Warehouse Carrier cannot be found with the code provided.")
            )

    @api.model
    def _update_pick_dict(self, row_dict, error_list, pick_dict, company):
        picking_ref = row_dict.get("picking_ref")
        picking = self.env["stock.picking"].search(
            [("name", "=", picking_ref), ("company_id", "=", company.id)]
        )
        if not picking:
            error_list.append(_("Designated delivery does not exist."))
        # 伝票番号一覧 data may contain multiple lines for a picking. (i.e. the lines
        # are as per the package). Therefore we need to avoid processing the same
        # picking multiple times here.
        elif picking not in pick_dict:
            pick_dict[picking] = {
                "tracking_refs": [picking.carrier_tracking_ref]
                if picking.carrier_tracking_ref
                else []
            }
            if picking.state in ("draft", "cancel", "done"):
                error_list.append(
                    _("Delivery is not in the right state (Draft/Done/Cancelled).")
                )
            elif picking.state != "assigned":
                picking.action_assign()
                if picking.state != "assigned":
                    error_list.append(_("Not enough stock is available."))
            # We assume that there is only one warehouse carrier per picking.
            if row_dict.get("carrier_code"):
                self._update_pick_dict_carrier_info(
                    row_dict["carrier_code"], error_list, pick_dict, picking
                )
        if pick_dict and row_dict.get("tracking_ref"):
            # Avoid duplicates while respecting the existing carrier_tracking_ref value
            # in the picking if any.
            if row_dict["tracking_ref"] not in pick_dict[picking]["tracking_refs"]:
                pick_dict[picking]["tracking_refs"].append(row_dict["tracking_ref"])

    @api.model
    def _update_and_validate_picking(self, picking, vals, import_log):
        picking_vals = {"log_id": import_log.id}
        carrier_info = vals.get("carrier_info")
        if carrier_info:
            picking_vals["carrier_info_id"] = carrier_info.id
        tracking_refs = vals.get("tracking_refs")
        if tracking_refs:
            tracking_refs = ", ".join(ref for ref in list(set(tracking_refs)))
            picking_vals["carrier_tracking_ref"] = tracking_refs
        picking.write(picking_vals)
        picking.with_delay(
            description=_("%s: Validate Delivery") % picking.name
        )._validate_picking()

    def import_stock_delivery_result(self):
        import_log = self._create_import_log("stock.picking")
        field_defs = self._get_field_defs(FIELD_KEYS, FIELD_VALS)
        sheet_fields, csv_iterator = self._load_import_file(
            field_defs, ["shift-jis", "utf-8"]
        )
        company = self.env.user.company_id
        pick_dict = {}
        for row in csv_iterator:
            row_dict, error_list = self._check_field_vals(field_defs, row, sheet_fields)
            # Here is the module specific logic
            if row_dict:
                self._update_pick_dict(row_dict, error_list, pick_dict, company)
            if error_list:
                self.env["data.import.error"].create(
                    {
                        "log_id": import_log.id,
                        "row_no": csv_iterator.line_num,
                        "reference": row_dict.get("picking_ref", "N/A"),
                        "error_message": "\n".join(error_list),
                    }
                )
        if not import_log.error_ids:
            for picking, vals in pick_dict.items():
                self._update_and_validate_picking(picking, vals, import_log)
            import_log.sudo().write({"state": "imported"})
        return self._action_open_import_log(import_log)
