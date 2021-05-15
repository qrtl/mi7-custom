# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DataImportError(models.Model):
    _inherit = "data.import.error"

    picking_ref = fields.Char(string="Picking Reference")
    # warning_log_id = fields.Many2one("error.log", string="Log")
