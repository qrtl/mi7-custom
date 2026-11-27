# Copyright 2026 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    # Partners anonymized before the signup fields were cleared on deactivation.
    cr.execute(
        """
        UPDATE res_partner
        SET signup_token = NULL, signup_type = NULL, signup_expiration = NULL
        WHERE NOT active
            AND name = '退会済み ' || id
        """
    )
