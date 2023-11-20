This module does the following:

- Adds error_msg field to the payment acquirer model.
- Shows error_msg of the acquirer in the payment confirmation pages.

Individual acquirer module (or a bridge module) must extend
\_compute_show_error_msg() method to enable the field.
