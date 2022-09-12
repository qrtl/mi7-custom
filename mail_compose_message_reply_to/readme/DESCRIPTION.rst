This module does the following:

- Respects the 'reply-to' setting of the email template unless the value was otherwise specified.

This is to "fix" the standard behavior which we suspect to be a bug - even when 'reply-to' is set in the template.
it does not seem to be respected.
