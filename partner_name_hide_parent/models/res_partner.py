# Copyright 2020 Quartile Limited
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    hide_parent = fields.Boolean(
        help="If selected, the parent's name will not be included in the "
        "display name of self."
    )

    @api.multi
    def name_get(self):
        res = super(ResPartner, self).name_get()
        for partner in self:
            name = partner._get_name()
            if partner.hide_parent and partner.parent_id:
                name = name.replace(partner.parent_id.name + ", ", "")
            for item in res:
                if item[0] == partner.id:
                    res.remove(item)
            res.append((partner.id, name))
        return res

    # Just add "hide_parent" as a trigger.
    @api.depends(
        "is_company", "name", "parent_id.name", "type", "company_name", "hide_parent"
    )
    def _compute_display_name(self):
        return super(ResPartner, self)._compute_display_name()
