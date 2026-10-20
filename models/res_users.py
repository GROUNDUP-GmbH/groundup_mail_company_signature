# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright 2026 Ground UP GmbH

from odoo import api, fields, models
from odoo.tools import is_html_empty


class ResUsers(models.Model):
    _inherit = "res.users"

    company_signature_ids = fields.One2many(
        "res.users.signature",
        "user_id",
        string="Signatures per Company",
        copy=False,
    )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ["company_signature_ids"]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ["company_signature_ids"]

    def _get_signature_for_company(self, company):
        """Return the effective signature for ``company``.

        A company-specific signature wins when it exists and is not empty.
        The regular user signature is the fallback.
        """
        self.ensure_one()
        if company and company in self.sudo().company_ids:
            signature = self.env["res.users.signature"].sudo().search(
                [
                    ("user_id", "=", self.id),
                    ("company_id", "=", company.id),
                ],
                limit=1,
            )
            if signature and not is_html_empty(signature.signature):
                return signature.signature
        return self.signature

    @api.model
    def _init_store_data(self, store):
        """Expose the effective signature to the mail composer preview."""
        result = super()._init_store_data(store)
        user = self.env.user
        if not user._is_public():
            signature = user._get_signature_for_company(self.env.company)
            if signature:
                store.add_model_values(
                    "res.users",
                    {"id": user.id, "signature": signature},
                )
        return result
