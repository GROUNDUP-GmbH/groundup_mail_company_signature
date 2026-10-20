# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright 2026 Ground UP GmbH

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCompanySignature(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_a = cls.env["res.company"].create({"name": "Signature Company A"})
        cls.company_b = cls.env["res.company"].create({"name": "Signature Company B"})
        cls.company_c = cls.env["res.company"].create({"name": "Signature Company C"})
        cls.user = cls.env["res.users"].with_context(no_reset_password=True).create(
            {
                "name": "Multi Company Signature User",
                "login": "multi.company.signature@example.com",
                "email": "multi.company.signature@example.com",
                "company_id": cls.company_a.id,
                "company_ids": [(6, 0, [cls.company_a.id, cls.company_b.id])],
            }
        )
        cls.signature_a = cls.env["res.users.signature"].create(
            {
                "user_id": cls.user.id,
                "company_id": cls.company_a.id,
                "signature": "<p>Signature A</p>",
            }
        )
        cls.signature_b = cls.env["res.users.signature"].create(
            {
                "user_id": cls.user.id,
                "company_id": cls.company_b.id,
                "signature": "<p>Signature B</p>",
            }
        )

    def test_resolver_uses_company_signature(self):
        self.assertIn(
            "Signature A",
            str(self.user._get_signature_for_company(self.company_a)),
        )
        self.assertIn(
            "Signature B",
            str(self.user._get_signature_for_company(self.company_b)),
        )

    def test_resolver_falls_back_to_default(self):
        self.assertEqual(
            self.user._get_signature_for_company(self.company_c),
            self.user.signature,
        )

    def test_company_access_is_enforced(self):
        with self.assertRaises(ValidationError):
            self.env["res.users.signature"].create(
                {
                    "user_id": self.user.id,
                    "company_id": self.company_c.id,
                    "signature": "<p>Signature C</p>",
                }
            )

    def test_email_rendering_uses_company_signature(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Signature Customer A",
                "company_id": self.company_a.id,
            }
        )
        message = self.env["mail.message"].create(
            {
                "model": "res.partner",
                "res_id": partner.id,
                "author_id": self.user.partner_id.id,
                "body": "<p>Hello</p>",
                "message_type": "comment",
                "subtype_id": self.env.ref("mail.mt_comment").id,
                "email_add_signature": True,
            }
        )
        values = partner._notify_by_email_prepare_rendering_context(message)
        self.assertIn("Signature A", str(values["signature"]))
