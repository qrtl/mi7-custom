# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class TargetDatabase(models.Model):

    _name = "target.database"
    _description = "Base Uninstall Module"

    base_uninstall_module_id = fields.Many2one("base.uninstall.module")
    name = fields.Char
