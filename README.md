# Company-wise User Email Signature

Odoo stores one email signature per user. In a multi-company setup a user who
works for several companies usually needs a different signature per company.

This module adds a signature per user and company. The regular user signature
stays the default and is used as fallback.

## Behavior

- A company-specific signature wins when it exists and is not empty.
- The regular **Email Signature** on the user is the fallback.
- The signature is chosen from the record's company, or from the active company
  when the record has no company.
- The mail composer preview shows the effective signature. The server always
  renders the final email, so the sent signature is the company's signature.
- Single-company users see no extra field; the module is a no-op for them.

## Install

### Odoo.sh

The repository root is the addon. Add it as a submodule at the root of the
odoo.sh project repository, not inside a nested addons folder:

```bash
git submodule add https://github.com/GROUNDUP-GmbH/groundup_mail_company_signature.git \
    groundup_mail_company_signature
git submodule update --init --recursive
```

Pin the submodule to a release tag, push to the staging branch, then install:

```bash
odoo-bin -i groundup_mail_company_signature --stop-after-init
```

Test on a staging database copy before promoting to production. Updates use the
normal module upgrade (`-u groundup_mail_company_signature`) and a new submodule
pin.

### Odoo Community

Clone the repository into a directory on the addons path:

```bash
git clone https://github.com/GROUNDUP-GmbH/groundup_mail_company_signature.git
```

The addons path entry is the repository root. Install the module from Apps, or
with `odoo-bin -i groundup_mail_company_signature --stop-after-init`.

## Configuration

1. Open **Settings → Users & Companies → Users** and select a user.
2. In **Preferences**, edit **Signatures per Company**.
3. Add one row per company and write the signature.
4. Leave a company out (or leave its signature empty) to use the default
   signature.

Users can edit their own rows under **My Profile → Preferences**. Administrators
with **Settings** access can edit any user.

## Security

- Users can read, create, edit and delete only their own signature rows for
  companies they belong to.
- Settings administrators can manage all rows.
- A constraint rejects a row for a company the user cannot access.

## Known limitations

- Mail templates that deliberately embed `${object.user_id.signature}` in the
  template body use the default signature. The module changes the signature
  block that Odoo adds to outgoing notifications, not arbitrary template
  placeholders.
- Out-of-office auto-replies use the default signature in this version.
- If a user opens a record of a non-active company without switching the active
  company, the composer preview may show the active company's signature. The
  sent email still uses the record company's signature.

## Tests

```bash
odoo-bin -i groundup_mail_company_signature --test-enable --stop-after-init
```

## License

LGPL-3.0-or-later. See `LICENSE`.
