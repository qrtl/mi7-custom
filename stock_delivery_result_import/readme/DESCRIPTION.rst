This module does the following:

- Adds a CSV import function to validate the designated outgoing pickings.
- Updates the tracking reference of the picking with '伝票番号', which is taken from the imported CSV file.

This module depends on base_data_import module and queue_job module.
The status of an import log record becomes 'Done' when all the linked pickings
are successfully validated.
