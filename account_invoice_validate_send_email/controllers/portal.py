# Copyright 2021 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalAccount(CustomerPortal):
    def _show_report(self, model, report_type, report_ref, download=False):
        if report_ref == "account.account_invoices":
            template = model.company_id.invoice_mail_template_id
            if template and template.report_template:
                model_data_rec = (
                    request.env["ir.model.data"]
                    .sudo()
                    .search(
                        [
                            ("model", "=", "ir.actions.report"),
                            ("res_id", "=", template.report_template.id),
                        ]
                    )
                )
                if model_data_rec:
                    report_ref = model_data_rec.complete_name
        return super()._show_report(model, report_type, report_ref, download=download)
