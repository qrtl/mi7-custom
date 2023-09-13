# Copyright 2023 Quartile Limited

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    address_name_text = fields.Html(translate=True)
