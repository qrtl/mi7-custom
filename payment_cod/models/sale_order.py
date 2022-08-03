# Copyright 2018 Lorenzo Battistini - Agile Business Group
# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _needs_delivery(self):
        self.ensure_one()
        if self.order_line.filtered(
            lambda x: x.product_id.type in ("consu", "product")
        ):
            return True
        return False

    def _is_cod_available(self, acquirer):
        self.ensure_one()
        if not self._needs_delivery():
            return False
        order_amount = self.amount_total
        company = self.company_id or self.env.company
        if self.currency_id != company.currency_id:
            order_amount = self.currency_id._convert(
                order_amount,
                company.currency_id,
                company,
                self.date_order or fields.Date.today(),
            )
        if order_amount > acquirer.amount_limit:
            return False
        return True

    def create_fee_line(self, tx):
        self.ensure_one()
        self.order_line.filtered(lambda x: x.is_payment_fee).unlink()
        fee_product = tx.acquirer_id.fee_product_id
        if fee_product:
            fee_line = self.env["sale.order.line"].create(
                {
                    "order_id": self.id,
                    "is_payment_fee": True,
                    "product_id": fee_product.id,
                    "product_uom": fee_product.uom_id.id,
                    "name": fee_product.name,
                    "product_uom_qty": 1,
                }
            )
            fee_line.product_id_change()
            fee_line.write({"price_unit": tx.fees})
            return fee_line
        return False
