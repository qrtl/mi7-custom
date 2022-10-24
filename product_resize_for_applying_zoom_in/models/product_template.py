# Copyright 2022 Quartile Limited
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
import binascii
import io

from PIL import Image

from odoo import _, api, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        templates = super(ProductTemplate, self).create(vals_list)

        for template, vals in zip(templates, vals_list):
            related_vals = {}
            if "image_1920" in vals:
                buffer = io.BytesIO()
                file_image = base64.b64decode(vals["image_1920"])
                stream = io.BytesIO(file_image)
                img = Image.open(stream)
                width, height = img.size
                if width < 1025 and height < 1025:
                    if width > height:
                        difference = 1200 - width
                        resize_image = img.resize((1200, height + difference))
                    else:
                        difference = 1200 - height
                        resize_image = img.resize((width + difference, 1200))
                    resize_image.save(buffer, format="PNG")
                    resize_image_b64 = base64.b64encode(buffer.getvalue())
                    related_vals["image_1920"] = resize_image_b64
            if related_vals:
                template.write(related_vals)

        return templates

    def write(self, vals):
        if "image_1920" in vals:
            buffer = io.BytesIO()
            try:
                file_image = base64.b64decode(vals["image_1920"])
                stream = io.BytesIO(file_image)
                img = Image.open(stream)
            except (OSError, binascii.Error):
                img = False
            if not img:
                raise UserError(_("This file could not be decoded as an image file."))
            width, height = img.size
            if width < 1025 and height < 1025:
                if width > height:
                    difference = 1200 - width
                    resize_image = img.resize((1200, height + difference))
                else:
                    difference = 1200 - height
                    resize_image = img.resize((width + difference, 1200))
                resize_image.save(buffer, format="PNG")
                resize_image_b64 = base64.b64encode(buffer.getvalue())
                vals["image_1920"] = resize_image_b64
        res = super(ProductTemplate, self).write(vals)
        return res
