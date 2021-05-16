# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DataImportLog(models.Model):
    _inherit = "data.import.log"

    picking_ids = fields.One2many(
        "stock.picking", "log_id", string="Imported Deliveries"
    )
