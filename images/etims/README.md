# eTIMS documentation screenshots

The eTIMS guide references the images below. They are **placeholders** — capture each one from a running `sync2books-react` dashboard and drop the PNG here using the exact filename. Until a file exists, GitBook shows the alt text.

Capture at a consistent width (≈1440px), light theme, with realistic-but-fake data (no real KRA PINs or secrets — blur/redact any live API key or secret).

| File | Dashboard route | What to capture |
|------|-----------------|-----------------|
| `01-signup.png` | `/auth/signup` | The sign-up wizard (personal details + organization step). |
| `02-application-setup.png` | `/onboarding/application-setup` | The "create your first application" form during onboarding. |
| `03-organization-apps.png` | `/dashboard/organization` | The organization dashboard listing applications with status. |
| `04-api-keys.png` | `/dashboard/applications/{id}/api-keys` | The API Keys screen with the Development/Production toggle and the API key field. **Redact the secret values.** |
| `05-integrations-etims.png` | `/dashboard/applications/{id}/integrations` | The integrations list showing the eTIMS connector. |
| `06-company-provision.png` | company detail page (eTIMS provision card) | The per-company eTIMS provisioning card (KRA PIN input + provision button). Component: `components/etims-company-provision-card.tsx`. |
| `07-sync-monitoring.png` | `/dashboard/applications/{id}/sync-monitoring` | The sync monitoring view showing batches/items and any errors. |

After adding the files, the references in the `etims-*.md` pages render automatically — no path changes needed.
