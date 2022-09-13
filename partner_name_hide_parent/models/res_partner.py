# Copyright 2020-2022 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    hide_parent = fields.Boolean(
        help="If selected, the parent's name will not be included in the "
        "display name of self."
    )

    # Override the standard method
    def _get_contact_name(self, partner, name):
        # Following two lines are inserted. (QRTL)
        if partner.hide_parent:
            return name
        return super()._get_contact_name(partner,name)

    # Just add "hide_parent" as a trigger.
    @api.depends(
        "is_company", "name", "parent_id.name", "type", "company_name", "hide_parent"
    )
    def _compute_display_name(self):
        return super(ResPartner, self)._compute_display_name()
