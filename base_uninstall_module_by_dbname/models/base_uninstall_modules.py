# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
import re


class BaseUninstallModules(models.Model):

    _name = "base.uninstall.modules"
    _description = "Base Uninstall Modules"

    uninstall_module_ids = fields.One2many("ir.module.module")
    target_db_ids = fields.One2Many("target.database")

    @api.model
    def _get_db_name(self):
        db_name = self.env.cr.dbname
        for database in self.target_db_ids:
            db_regex = "^(?=.*" +str(database.name) + ").*$"
            if re.match(db_regex, db_name):
                for module in self.uninstall_module_ids:
                    self.env['ir.module.module'].search([('name', '=', str(module.name))]).button_immediate_uninstall()
