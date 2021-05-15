# -*- coding: utf-8 -*-
# Copyright 2020-2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DataImportError(models.Model):
    _name = "data.import.error"

    row_no = fields.Integer("Row Number")
    error_message = fields.Text("message")
    log_id = fields.Many2one("data.import.log", string="Log")
