# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright 2026 Ground UP GmbH

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResUsersSignature(models.Model):
    _name = "res.users.signature"
    _description = "User Email Signature per Company"
    _order = "company_id, user_id"

    user_id = fields.Many2one(
        "res.users",
        string="User",
        required=True,
        ondelete="cascade",
        index=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        ondelete="cascade",
        index=True,
    )
    signature = fields.Html(
        string="Email Signature",
        sanitize=True,
    )

    _uniq_user_company = models.Constraint(
        "UNIQUE(user_id, company_id)",
        "A user can have only one email signature per company.",
    )

    @api.constrains("user_id", "company_id")
    def _check_company_access(self):
        for record in self:
            if (
                record.user_id
                and record.company_id
                and record.company_id not in record.user_id.company_ids
            ):
                raise ValidationError(
                    _("The user must have access to the company of the signature.")
                )
