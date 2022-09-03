This module does the following:

* Updates date_order of the eCommerce order to the current date at following points:

  * When an eCommerce related page is loaded and date_order is different to the current
    date.
  * When the eCommerce payment goes through validation steps (i.e.
    /shop/payment/validate) after pressing the Pay Now button.
