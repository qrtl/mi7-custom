This module adds a script in the /shop/confirmation page to pass the
relevant sales data to A8, an affiliate service provider.

- Capture a8_param from the cookie and saves it in the partner at user
  login.
- Generates a cookie with A8 param based on the partner's a8_param at
  the time of checkout.
- Extends the template of /shop/confirmation page to set A8's JavaScript
  and sales contents.
- Clears a8_param of the partner with payment confirmation.

Currencies supported by A8: JPY, USD, and EUR

## Caveats

Currently the A8 affiliate sales is NOT recognized for if customer takes
following operation sequence:

1.  Customer is already logged in to the eCommerce shop.
2.  Customer clicks an A8 link to arrive at the shop (no login step
    since already logged in). When this happens, the user is not updated
    with the A8 param.
3.  Customer logs in to the shop from another device/browser to proceed
    with an order.
