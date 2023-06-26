# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailMessageSubtype(models.Model):
    _inherit = "mail.message.subtype"

    allow_send_model_ids = fields.Many2many("ir.model")
