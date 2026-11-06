This module enables portal users to deactivate their accounts by
themselves.

On deactivation, the user is archived and then deleted, and the personal
data of the user's partner and its child addresses (e.g. delivery
addresses) is erased:

- The name is replaced with `退会済み <partner ID>` (e.g. `退会済み 12345`),
  as a contact requires a name.
- Email, phone, mobile, address, furigana, gender, birthday and image are
  cleared, and the partners are archived.
- The chatter of these partners (messages including tracking values,
  followers, activities and attachments) is deleted.
- In their payment transactions, the name, email, phone and address are
  cleared. The amount, dates, state and links to sales orders are kept.

The following are not modified: department, occupation, comment, saved
payment tokens, sales orders, invoices and their chatter. For a contact
under a company, the parent company and its other contacts and addresses
are left untouched.

Sales orders and invoices refer to the partner for the name and address,
so they show the anonymized values once the account is deactivated.

The account cannot be deactivated from the portal, and the user is asked
to contact the company instead, when:

- the user's partner is B2B (User Type),
- the partner is an address of another partner (e.g. a delivery address
  with its own login),
- a contact (archived ones included) is registered under the partner or
  its addresses, or
- another active user is linked to the partner or its addresses.

The last three conditions keep the deactivation from reaching other
people's records when the User Type is wrong.
