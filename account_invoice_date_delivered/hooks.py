# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo.tools import column_exists

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """Allow installing the module in a database with large account.move and
    account.move.line tables by skipping the computation.
    """
    if not column_exists(cr, "account_move", "time_delivered"):
        _logger.info("Creating account.move columns with null values.")
        cr.execute(
            """
            ALTER TABLE "account_move"
            ADD COLUMN "time_delivered" timestamp,
            ADD COLUMN "date_delivered" date
        """
        )
    if not column_exists(cr, "account_move_line", "time_delivered"):
        _logger.info("Creating account.move.line columns with null values.")
        cr.execute(
            """
            ALTER TABLE "account_move_line"
            ADD COLUMN "time_delivered" timestamp,
            ADD COLUMN "date_delivered" date
        """
        )
