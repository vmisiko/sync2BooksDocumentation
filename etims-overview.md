# eTIMS Compliance Overview

Sync2Books lets you connect your invoicing system to **KRA eTIMS** without building against KRA yourself. We handle the eTIMS device protocol, signing, receipts, and the mandatory KRA sequence behind a simple API. You integrate once with Sync2Books and your invoices become tax-compliant.

> **Who this is for.** You are a developer at a business (or building software for businesses) that invoices in Kenya and needs eTIMS compliance. Instead of going through KRA certification, device setup, and the eTIMS spec, you connect your company once in our **dashboard** and then push items, stock, and sales through our **API**.

## The two surfaces: Dashboard vs API

This is the key idea. Setup is no-code in the dashboard; daily operations are programmatic via the API.

| | **Dashboard** (one-time, no-code) | **API** (ongoing, programmatic) |
|---|---|---|
| Create your application & get API keys | ✅ | |
| **Connect a company to eTIMS** (KRA PIN, device, branch) | ✅ | (advanced/optional) |
| Manage the connection & view status | ✅ | |
| **Register & sync catalog items** | | ✅ |
| **Create sales & credit notes** | | ✅ |
| **Adjust & transfer stock** | | ✅ |
| Monitor results | ✅ | ✅ |

In short: **the dashboard handles eTIMS onboarding; your code handles invoicing.** You never have to script KRA onboarding to get going.

## What you can do through the API

Once a company is connected (in the dashboard), your application can:

- **Register a product catalog** and sync items to eTIMS (so they can be invoiced)
- **Manage stock** — adjust levels and transfer between branches
- **Create sales** and receive a signed KRA receipt (ETR number)
- **Issue credit notes** against accepted sales
- **Read back** catalog and sales data for reconciliation

Everything runs server-to-server with your API key. No browser, no device, no KRA portal in your request path.

## How it works

You make one kind of request — to the Sync2Books API, with your API key:

```
┌──────────────────┐        ┌──────────────┐        ┌────────────┐
│  Your application │  HTTP  │  Sync2Books  │  eTIMS │  KRA eTIMS │
│  (uses API key)   │ ─────▶ │     API      │ ─────▶ │            │
│                   │ ◀───── │              │ ◀───── │            │
└──────────────────┘        └──────────────┘        └────────────┘
```

You call `…/companies/{companyId}/integrations/etims/…` with your API key; Sync2Books does the eTIMS work with KRA and returns the result. Most operations are **asynchronous**: you get a `syncBatchId` immediately and confirm the outcome shortly after (see [Tracking Results](./etims-tracking-results.md)).

## The entities you'll touch

| Entity | What it is | Created via |
|--------|------------|-------------|
| **Company** | A business entity you're invoicing for | API or dashboard |
| **eTIMS connection** | The provisioned link to KRA (KRA PIN, branch, device) | **Dashboard** |
| **Catalog item** | A good (stock-tracked) or service (non-stock) that can be invoiced | API |
| **Sale** | An invoice submitted to eTIMS; yields a signed receipt | API |
| **Credit note** | A reversal against an accepted sale | API |
| **Sync batch** | The async tracking record for any operation | returned as `syncBatchId` |

## Prerequisites

To go live against **production** eTIMS, the business must complete KRA's onboarding (so it has a KRA PIN, branch, and device). That KRA-side process — and where the values you enter when connecting come from — is documented in **[eTIMS as a Third-Party Integrator (OSCU)](./ETIMS_OSCU_INTEGRATION_AS_THIRD_PARTY.md)**.

To start building and testing, you only need:

- ✅ A Sync2Books **account, organization, and application** (created in the dashboard)
- ✅ Your application's **API key**
- ✅ A company **connected to eTIMS in the dashboard** (sandbox values are fine while developing)

## Where to go next

1. **[Get Started with eTIMS](./etims-getting-started.md)** — set up in the dashboard, then run your first sale via the API
2. **[Postman Collection](./etims-postman.md)** — import every eTIMS request and start calling in minutes
3. **[Connecting a Company](./etims-provisioning.md)** — connect a company to eTIMS (dashboard)
4. **[Catalog](./etims-catalog.md)** — register and sync items (API)
5. **[Sales & Credit Notes](./etims-sales.md)** — invoice and reverse (API)
6. **[Stock](./etims-stock.md)** — adjust and transfer inventory (API)
7. **[Tracking Results](./etims-tracking-results.md)** — the async model
8. **[API Reference](./etims-api-reference.md)** — every endpoint and field
