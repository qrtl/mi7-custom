This module does the following:

- When customer invoice that meets the following condition is validated, Odoo will print and send the invoice to the followers of the document.
  - 'Invoice Sent' is not flagged (the field is flagged when the invoice is sent by the module logic).
  - 'Send Invoice upon Validation' is set in the workflow process linked to the invoice.

The module depends on the OCA module sale_automatic_workflow.
