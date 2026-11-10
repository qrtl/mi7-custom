# Copyright 2026 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).


def migrate(cr, version):
    # Partners whose birthday was cleared before the compute fix kept their old month.
    cr.execute(
        """
        UPDATE res_partner
        SET birth_month = 0
        WHERE birthday IS NULL AND COALESCE(birth_month, 0) <> 0
        """
    )
