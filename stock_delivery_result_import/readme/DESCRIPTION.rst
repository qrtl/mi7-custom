This module does the following:

- Adds a CSV import function to validate the designated outgoing pickings.
- Compute and add a carrier_tracking_ref add into stock_picking.

This module depends on base_data_import module and queue_job module.
The status of an import log record becomes 'Done' when all the linked pickings
are successfully validated.
