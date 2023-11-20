This module does the following:

- Provides the function of rounding down the tax amount in the invoice,
  covering:
  - the total presentation in invoice form/print
  - the tax amount calculation of account move line

Note that, due to the structure of compute_all() method, the round-down
does not work perfectly in case the document involves multiple taxes
with different price_include settings (which is not expected to happen
under normal circumstances in the Japanese business environment).

## Background:

In Japan there is sometimes a tacit industry-wide convention of rounding
down the tax amount instead of applying the default rounding
("HALF-UP").
