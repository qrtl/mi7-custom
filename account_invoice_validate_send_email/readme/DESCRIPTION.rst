This module does the following:
- Add slip_number field in account_invoice model. Compute by stock_picking.carrier_tracking_ref field numbers.

- When customer invoice that meets all of the following conditions is validated, Odoo will print and send the invoice to the followers of the document.
  - 'Send Invoice upon Validation' is set in the workflow process linked to the invoice.
  - 'Not Auto-send Invoice' of the pikcing linked to the invoice is not selected.
  - 'Not Auto-send Invoice' of the payment term assigned to the invoice is not selected.
  - 'Invoice Sent' is not flagged (the field is flagged when the invoice is sent by the module logic).

The module depends on the OCA module sale_automatic_workflow.
