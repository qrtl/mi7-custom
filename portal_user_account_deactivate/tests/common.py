# Copyright 2026 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import new_test_user

# 1x1 PNG
IMAGE = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAA"
    "SUVORK5CYII="
)


class AccountDeactivateCommon:
    @classmethod
    def _setup_account_deactivate_data(cls):
        cls.country = cls.env.ref("base.jp")
        cls.state = cls.env["res.country.state"].search(
            [("country_id", "=", cls.country.id)], limit=1
        )
        cls.address_vals = {
            "street": "1-2-3 Test",
            "street2": "Test Building",
            "zip": "1000001",
            "city": "Chiyoda",
            "state_id": cls.state.id,
            "country_id": cls.country.id,
        }
        cls.user = new_test_user(
            cls.env, login="deactivate_b2c", groups="base.group_portal"
        )
        cls.partner = cls.user.partner_id
        cls.partner.write(
            dict(
                cls.address_vals,
                name="Taro Yamada",
                email="taro@example.com",
                phone="03-0000-0000",
                mobile="090-0000-0000",
                furigana="ヤマダ タロウ",
                gender="male",
                birthday="1990-05-01",
                image_1920=IMAGE,
                department="Sales",
                comment="Note kept after deactivation",
            )
        )
        cls.delivery = cls.env["res.partner"].create(
            dict(
                cls.address_vals,
                name="Taro Yamada (Home)",
                parent_id=cls.partner.id,
                type="delivery",
                email="taro.home@example.com",
                phone="03-1111-1111",
                mobile="090-1111-1111",
            )
        )
        cls.archived_delivery = cls.env["res.partner"].create(
            dict(
                cls.address_vals,
                name="Taro Yamada (Old)",
                parent_id=cls.partner.id,
                type="delivery",
                active=False,
            )
        )
