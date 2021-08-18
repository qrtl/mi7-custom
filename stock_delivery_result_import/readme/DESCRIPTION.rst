This module does the following:

- Adds a CSV import function to validate the designated outgoing pickings.
- Adds a slip_number field in account_invoice model.

This module depends on base_data_import module and queue_job module.
The status of an import log record becomes 'Done' when all the linked pickings
are successfully validated.
