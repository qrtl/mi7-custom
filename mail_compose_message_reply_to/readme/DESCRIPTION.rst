This module does the following:

- If a mail template was arranged, Odoo will automatically set the reply_to address when send mails.

This is to "fix" the standard behavior which we suspect to be a bug - even when 'reply-to' is set in the template.
it does not seem to be respected.
