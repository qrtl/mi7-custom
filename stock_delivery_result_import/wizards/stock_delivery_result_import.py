# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, models

FIELD_KEYS = {0: "field", 1: "label", 2: "field_type", 3: "required"}
# Prepare values corresponding with the keys
FIELD_VALS = [
    ["picking_ref", "受注番号", "char", True],
]


class StockDeliveryResultImport(models.TransientModel):
    _name = "stock.delivery.result.import"
    _inherit = "data.import"

    def import_stock_delivery_result(self):
        picking_obj = self.env["stock.picking"]
        import_log = self._create_import_log("stock.picking")
        field_defs = self._get_field_defs(FIELD_KEYS, FIELD_VALS)
        sheet_fields, csv_iterator = self._load_import_file(
            field_defs, ["shift-jis", "utf-8"]
        )
        track_ref_field = [["carrier_tracking_ref", "伝票番号", "char", False]]
        update_field = self._get_field_defs(FIELD_KEYS, track_ref_field)
        company = self.env.user.company_id
        pickings = picking_obj.browse([])
        for row in csv_iterator:
            row_dict, error_list = self._check_field_vals(field_defs, row, sheet_fields)
            row_update, update_error_list = self._check_field_vals(
                update_field, row, sheet_fields
            )
            # Here is the module specific logic
            if row_dict and not error_list and not update_error_list:
                picking_ref = row_dict.get("picking_ref")
                picking = picking_obj.search(
                    [("name", "=", picking_ref), ("company_id", "=", company.id)]
                )
                carrier_tracking_ref = row_update.get("carrier_tracking_ref")
                if not picking:
                    error_list.append(_("Designated delivery does not exist."))
                # 伝票番号一覧 data may contain multiple lines for a picking. (i.e. the lines
                # are as per the package). Therefore we need to avoid processing the same
                # picking multiple times here.
                elif picking not in pickings:
                    if picking.state in ("draft", "cancel", "done"):
                        error_list.append(
                            _(
                                "Delivery is not in the right state (Draft/Done/Cancelled)."
                            )
                        )
                    else:
                        if picking.state in ("confirmed", "partially_available"):
                            picking.action_assign()
                        if not picking.state == "assigned":
                            error_list.append(_("Not enough stock is available."))
                    if not error_list:
                        picking.carrier_tracking_ref = carrier_tracking_ref
                        pickings += picking
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
            for picking in pickings:
                picking.log_id = import_log
                picking.with_delay(
                    description=_("%s: Validate Delivery") % picking.name
                )._validate_picking()
            import_log.sudo().write({"state": "imported"})
        return self._action_open_import_log(import_log)
