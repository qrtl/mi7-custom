This module does the following:

- Adds error_msg field to the payment acquirer model.

This module does not do anything by itself. Individual acquirer module (or a bridge
module must extend _compute_show_error_msg() method to enable the field.
