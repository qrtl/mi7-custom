# -*- coding: utf-8 -*-
# Copyright 2021 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
import re


class BaseUninstallModules(models.Model):

    _name = "base.uninstall.modules"
    _description = "Base Uninstall Modules"

    module_ids = fields.One2many("ir.module.module")
    target_database_ids = fields.One2many("target.database")

    @api.model
    def _get_db_name(self):
        db_name = self.env.cr.dbname
        for database in self.target_database_ids:
            db_regex = "^(?=.*" +str(database.name) + ").*$"
            if re.match(db_regex, db_name):
                for module in self.module_ids:
                    self.env['ir.module.module'].search([('name', '=', str(module._name))]).button_immediate_uninstall()
