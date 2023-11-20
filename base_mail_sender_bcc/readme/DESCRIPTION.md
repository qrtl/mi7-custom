This module does the following when an email is being built:

- Sets the same value as 'Reply To' in 'Bcc' if 'Reply To' is available.
- Otherwise, populates 'Bcc' based on the system parameter setting (key:
  email_bcc).

The module was originally created by Akretion
<https://apps.odoo.com/apps/modules/10.0/base_mail_sender_bcc/> and
adjusted by Quartile limited.
