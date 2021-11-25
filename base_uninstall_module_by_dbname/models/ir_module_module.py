# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    base_uninstall_module_id = fields.Many2one("base.uninstall.modules")
