# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleWorkflowProcess(models.Model):
    _inherit = "sale.workflow.process"

    send_invoice = fields.Boolean(string="Send Invoice upon Validation")
