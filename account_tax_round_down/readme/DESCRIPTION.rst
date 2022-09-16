This module does the following:

- Provides the function of rounding down the tax amount in the invoice.

_need_tax_round_down() method can be extended in another module in case there is a need
of applying the round-down based on certain conditions.

Background:
-----------

In Japan there is sometimes a tacit industry-wide convention of rounding down the tax
amount instead of applying the default rounding ("HALF-UP").
