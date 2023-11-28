# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    invoice_mail_template_id = fields.Many2one(
        "mail.template", string="Invoice Email Template"
    )
    invoice_mail_template_b2c_id = fields.Many2one(
        "mail.template", string="Invoice Mail Template (B2C)"
    )
