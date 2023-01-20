from odoo import api, fields, models
from odoo.tools.translate import html_translate


class ProductTemplate(models.Model):
    _inherit = [
        "product.template",
    ]

    @api.depends_context("uid")
    def _compute_can_write(self):
        writable_templates = self._filter_access_rules("write")
        for template in self:
            template.can_write = template in writable_templates

    website_description = fields.Html(
        "Description for the website",
        render_engine="qweb",
        sanitize_attributes=False,
        translate=html_translate,
        sanitize_form=False,
    )
    can_write = fields.Boolean(
        compute="_compute_can_write", help="The current user can edit the template."
    )
