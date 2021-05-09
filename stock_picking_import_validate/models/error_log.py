# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ErrorLog(models.Model):
    _inherit = "error.log"

    picking_ids = fields.One2many(
        "stock.picking", "log_id", string="Processed Pickings"
    )
    # warning_log_line_ids = fields.One2many(
    #     "error.log.line", "warning_log_id", string="Warning Log Lines"
    # )
