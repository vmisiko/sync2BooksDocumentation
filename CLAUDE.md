# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is the public Sync2Books documentation site, built with Mintlify (`docs.json`, `theme: mint`). It's content-only — no `package.json` or build tooling is checked in. To preview locally: `npm i -g mintlify` then `mintlify dev` from this directory.

## Structure

Navigation is defined in `docs.json` with two top-level tabs:
- **Documentation**: Get started (`index`, `quickstart`) → Core concepts (`concepts/`: authentication, companies-and-connections, sync-model, environments, errors-and-rate-limits) → Expenses (7 pages) → eTIMS compliance/Kenya (10 pages, including `ETIMS_OSCU_INTEGRATION_AS_THIRD_PARTY.mdx`) → Accounting integrations (`integrations/quickbooks-online/`, `integrations/odoo/`) → Link component.
- **API reference**: `api-reference.mdx` (mostly a pointer to the external Swagger UI at `api.sync2books.com/docs`) and `etims-api-reference.mdx`.

A Postman collection backing `etims-postman.mdx` is checked in at `etims-postman-collection.json` (and duplicated under `assets/`) — keep both in sync if updating one.

`api-reference.mdx` still references "This GitBook" — a leftover from a prior GitBook-based docs site that hasn't been cleaned up for the Mintlify migration; fix it if you're touching that page, otherwise it's fine to leave.

When editing, match the existing `.mdx` structure/frontmatter of neighboring pages in the same section rather than introducing a new format.
