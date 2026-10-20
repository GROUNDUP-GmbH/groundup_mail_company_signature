# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright 2026 Ground UP GmbH
{
    "name": "Company-wise User Email Signature",
    "version": "19.0.1.1.1",
    "category": "Productivity/Discuss",
    "summary": "Per-company email signatures for users working in several companies",
    "description": """
Company-wise User Email Signature
=================================

Odoo stores one email signature per user. In a multi-company setup a user who
works for several companies usually needs a different signature per company.

This module adds a signature table per user and company. The regular user
signature remains the default and is used as fallback. When Odoo renders an
outgoing email, the signature of the record's company (or the active company)
is used.

The module is standalone and has no Enterprise dependency. It can be installed
on Odoo Community and on Odoo.sh.
""",
    "author": "Ground UP GmbH",
    "website": "https://groundup.farm",
    "license": "LGPL-3",
    "depends": ["mail"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/res_users_views.xml",
    ],
    "installable": True,
    "application": False,
}
