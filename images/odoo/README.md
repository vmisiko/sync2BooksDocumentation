# Odoo documentation screenshots

Unlike the eTIMS placeholders, these are **real captures** from a fresh, disposable Odoo
18 instance (self-hosted, Docker) — not mockups. Captured via a scripted Playwright
walkthrough at 1280x900, light theme, fake demo data (`admin@example.com`, database
`my-company`). The instance was torn down immediately after capture.

The generated API key in `06-copy-key-once.png` is **redacted** (blacked out) even though
it came from a disposable local instance nobody could ever reach — matching this repo's
existing convention (see `images/etims/README.md`) of never showing secret values in
documentation, real or fake.

| File | What it shows |
|------|----------------|
| `01-create-database.png` | Odoo's self-hosted database creation screen, with the **Database Name** field filled in. |
| `02-user-menu-preferences.png` | The account dropdown open, showing the path to **Preferences**. |
| `03-account-security-new-api-key.png` | The **Account Security** tab, with the **New API Key** button. |
| `04-confirm-password.png` | Odoo's password re-confirmation dialog before generating a key. |
| `05-name-key-set-expiry.png` | The New API Key dialog — note the **1 Day** default validity duration, the most common setup mistake. |
| `06-copy-key-once.png` | The generated key screen (key redacted) — Odoo shows it exactly once. |

Referenced from `integrations/odoo/odoo-setup.mdx`. If Odoo's UI changes in a future
version, recapture using the script pattern rather than hand-editing — see
`nest-sync-2-books-api/.docs/ODOO_CONNECTOR_SETUP_GUIDE.md` for the equivalent
engineering-facing walkthrough this was captured alongside.
