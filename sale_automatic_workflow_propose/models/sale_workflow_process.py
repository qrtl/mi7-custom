# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleWorkflowProcess(models.Model):
    _inherit = "sale.workflow.process"

    # Keep the selectons consistent with user_type of sale.order
    apply_to = fields.Selection(
        [("b2c", "B2C"), ("b2b", "B2B")],
        help="The workflow process will be proposed to the sales orders of the "
        "selected order type here.",
    )
