# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright 2026 Ground UP GmbH

from markupsafe import Markup

from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _notify_by_email_prepare_rendering_context(
        self,
        message,
        msg_vals=False,
        model_description=False,
        force_email_company=False,
        force_email_lang=False,
        force_record_name=False,
    ):
        values = super()._notify_by_email_prepare_rendering_context(
            message,
            msg_vals=msg_vals,
            model_description=model_description,
            force_email_company=force_email_company,
            force_email_lang=force_email_lang,
            force_record_name=force_record_name,
        )
        author = values.get("author_user")
        if author and values.get("email_add_signature"):
            signature = author._get_signature_for_company(values.get("company"))
            values["signature"] = Markup("<div>-- <br/>%s</div>") % Markup(
                signature or ""
            )
        return values
