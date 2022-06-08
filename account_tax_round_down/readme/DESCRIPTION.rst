This module does the following:

- Provides the base function of rounding down the tax amount in the invoice depending
  on the given conditions which should be provided another module by extending the
  _need_tax_round_down() method.

Installing the module does not do anything by itself.

Background:

In Japan there is sometimes a tacit industry-wide convention of rounding down the tax
amount instead of applying the default rounding ("HALF-UP").
