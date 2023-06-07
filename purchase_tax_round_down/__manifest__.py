# Copyright 2022 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Tax Round Down",
    "version": "15.0.1.0.0",
    "category": "Tools",
    "license": "AGPL-3",
    "author": "Quartile Limited",
    "website": "https://www.quartile.co",
    "depends": [
        "purchase",
        "account_tax_round_down",
    ],
    "post_load": "post_load_hook",
    "installable": True,
}
