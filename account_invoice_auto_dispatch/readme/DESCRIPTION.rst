This module does the following:

- When customer invoice that meets the following condition is validated, Odoo will print and send the invoice to the followers (including the customer).
- Add  field `invoice_sent` boolean field to account.invoice to indicate whether the invoice has already been sent to the customer once, since there can be situations where user wants to modify the content by putting the document back to draft upon cancelling and re-validate the invoice later on.
