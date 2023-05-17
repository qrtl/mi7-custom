This module sends new separate mail for the entire description if there is other information
in description (custom input in website form).

Background
~~~~~~~~~~

When a visitor submits a online form, an auto-reply email is sent out to the visitor,
however the message body does not include the custom content from the form due to the
process sequence in _insert_record() method of WebsiteForm.

This causes inconvenience when you expect to be able to search the created Odoo record by
custom content using base_search_mail_content.  This module intends to get rid of this
inconvenience by adding to the record a message with custom content.
