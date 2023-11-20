This module does the following:

- Adds the delivery date and time fields in sale.order.
- Updates commitment_date of the order when delivery date is selected,
  based on the delivery date and the warehouse.shipping.delay parameter
  setting, so that the delivery schedule is adjusted accordingly.
