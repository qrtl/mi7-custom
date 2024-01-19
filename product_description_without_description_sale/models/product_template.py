# Copyright 2024 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    use_description_sale = fields.Boolean(
        "Use Sales Description",
        help="If selected, Sales Description will be appended "
        "to the sales order line description.",
        default=lambda self: self._default_use_description_sale(),
    )

    @api.model
    def _default_use_description_sale(self):
        # Get the system parameter configuration
        param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "product_description_without_description_sale.default_use_description_sale"
            )
        )
        if param == "1":
            return True
        return False
