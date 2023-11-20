This module does the following:

- Cancels other existing sales orders of the user when an order is
  created in the shop frontend operation.

There are cases where a new order is created while there is an existing
order (i.e. user added a product to the cart as a public user, and then
logged in while he/she had already added something in the cart), which
could lead to some problematic behaviors such as the user seeing
products in the cart right after processing an order.
