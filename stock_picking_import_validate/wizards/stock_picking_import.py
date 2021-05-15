# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, models

FIELD_KEYS = {0: "field", 1: "label", 2: "field_type", 3: "required"}
# Prepare values corresponding with the keys
FIELD_VALS = [
    ["picking_ref", "出荷指示番号", "char", True],
]


class StockPickingImport(models.TransientModel):
    _name = "stock.picking.import"
    _inherit = "data.import"

    def import_stock_picking(self):
        picking_obj = self.env["stock.picking"]
        import_log = self._create_import_log("stock.picking")
        field_defs = self._get_field_defs(FIELD_KEYS, FIELD_VALS)
        sheet_fields, csv_iterator = self._load_import_file(field_defs, ["shift-jis", "utf-8"])
        company = self.env.user.company_id
        pickings = picking_obj.browse([])
        for row in csv_iterator:
            row_dict, error_list = self._check_field_vals(field_defs, row, sheet_fields)
            # Here is the module specific logic
            if row_dict and not error_list:
                picking_ref = row_dict.get("picking_ref")                
                picking = picking_obj.search(
                    [
                        ("name", "=", picking_ref),
                        ("company_id", "=", company.id)
                    ]
                )
                if not picking:
                    error_list.append(_("Designated delivery does not exist."))
                else:
                    if picking.state in ("draft", "cancel", "done"):
                        error_list.append(_("Delivery is not in the right state (Draft/Done/Cancelled)."))
                    else:
                        if picking.state in ("confirmed", "partially_available"):
                            picking.action_assign()
                        if not picking.state == "assigned":
                            error_list.append(_("Not enough stock is available."))
                    if not error_list:
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
                picking.with_delay(description=_("%s: Validate Delivery") % picking.name)._validate_picking()
            import_log.sudo().write({"state": "imported"})
        return self._action_open_import_log(import_log)
