from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalAccount(CustomerPortal):
    MANDATORY_BILLING_FIELDS = ["name", "email"]
    OPTIONAL_BILLING_FIELDS = [
        "zipcode",
        "state_id",
        "vat",
        "company_name",
        "phone",
        "street",
        "city",
        "country_id",
    ]
