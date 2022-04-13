This module does the following:

- Blocks signups with suspicious names (i.e. 'http' is included).

This is to block malicious operators from sending out their phishing URLs to random
email addresses through Odoo - they may set their URL to the name field of the signup
page, which sends out an email (with a signup token) to the specified email address.
