This module does the following:

- Provides the base function of rounding down the tax amount in the invoice depending
  on the given conditions which should be provided another module by extending the
  _need_round_down() method.

Background:

In Japan there is sometimes a tacit industry-wide convention of rounding down the tax
amount instead of applying the default rounding ("HALF-UP").
