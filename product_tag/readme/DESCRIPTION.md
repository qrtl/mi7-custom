This module backports the `product.tag` model from Odoo 16, allowing
products to be classified with tags in Odoo 15.

Unlike the original Odoo 16 design, the implementation has been simplified: tags can
only be assigned at the product template (`product.template`) level, and not at the
product variant (`product.product`) level.
