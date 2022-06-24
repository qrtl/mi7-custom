This module does the following:

- Adds time_delivered and date_delivered fields to account.invoice, which should be
  populated for customer invoices based on the linked pickings.

The intention of having the date_delivered field (date type) is so that it will be easy
for users to see the date according to their timezone when the data are exported.

The module depends on the OCA module stock_picking_invoice_link.
