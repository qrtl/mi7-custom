This module enables portal users to deactivate their accounts by
themselves.

On deactivation, the user is archived and then deleted, and the personal
data of the user's partner and its child contacts (e.g. delivery
addresses) is erased:

- The name is replaced with "退会済み <partner ID>", as a contact
  requires a name.
- Email, phone, mobile, address, furigana, gender, birthday and image are
  cleared, and the partners are archived.
- The chatter of these partners (messages including tracking values,
  followers, activities and attachments) is deleted.
- In their payment transactions, the name, email, phone and address are
  cleared. The amount, dates, state and links to sales orders are kept.

The following are not modified: department, occupation, comment, saved
payment tokens, sales orders, invoices and their chatter. For a B2B user,
the parent company and the other contacts of the company (colleagues and
the company's delivery addresses) are left untouched.

Sales orders and invoices refer to the partner for the name and address,
so they show the anonymized values once the account is deactivated.
