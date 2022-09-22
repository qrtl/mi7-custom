This module does the following:

- Hides 'Be notified when back in stock' button in the wishlist
- Disables the cron 'Wishlist: send email regarding products availability'.
- Adjusts the logic to not select stock_notification when a product is added to the
  wishlist (to avoid the situation of notificaton emails accidentally shooting out when
  the cron is re-enabled).

Note that when the module is uninstalled, the disabled cron should manually be set back
to active as necessary.
