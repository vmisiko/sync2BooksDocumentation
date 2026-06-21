# eTIMS Postman Collection

A ready-to-run Postman collection with every operational eTIMS request — catalog, stock, and sales — so you can start calling the API in minutes.

## Download

📥 **[Download the eTIMS Postman collection](./etims-postman-collection.json)**

> Tip for maintainers: publish this collection to your Postman workspace to get a public **“Run in Postman”** button and a shareable link, then drop the button here:
> `[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/<your-collection-id>)`

## What's inside

| Folder | Requests |
|--------|----------|
| **Setup** | Create company · Provision eTIMS *(advanced — usually done in the dashboard)* |
| **Catalog** | Register item · List items · Sync items to eTIMS |
| **Stock** | Adjust stock (ADD/DEDUCT) · Transfer stock |
| **Sales** | Create sale · List sales · Get sale · Express credit note |

Authentication is preconfigured: the collection sends your key in the `X-API-Key` header on every request.

## Import & configure (2 minutes)

1. In Postman: **Import → File** → select `etims-postman-collection.json`.
2. Open the collection's **Variables** tab and set:

   | Variable | Set to | Where to get it |
   |----------|--------|-----------------|
   | `baseUrl` | `https://api.sync2books.com` | (already set) |
   | `apiKey` | your `sk_development_…` key | Dashboard → Application → API Keys |
   | `companyId` | your company id | Dashboard, or **Create company** response |
   | `branchId` | `HQ` | the branch key from provisioning |
   | `itemId` | *(fill after step below)* | **List items** response (`id`) |
   | `saleId` | *(fill after step below)* | **Create sale** → accepted document id |

3. Make sure the company is **connected to eTIMS** (provision it in the dashboard first — see [Provisioning](./etims-provisioning.md)).

## Suggested run order

The requests have prerequisites — run them in this order the first time:

```
1. Catalog → Register catalog item        → returns { syncBatchId }
2. Catalog → List catalog items           → copy an item id into {{itemId}}
3. Catalog → Sync items to eTIMS          → item becomes REGISTERED (sellable)
4. Stock   → Adjust stock (ADD)           → seed inventory (GOODS only; skip for SERVICE)
5. Sales   → Create sale                  → returns { syncBatchId }
6. Sales   → List sales                   → find ACCEPTED + etimsReceiptNumber; copy id into {{saleId}}
7. Sales   → Express credit note (optional)
```

> Most write requests are **asynchronous** — they return a `syncBatchId` and the result is confirmed shortly after. Use **List items** / **List sales** to confirm the outcome. See [Tracking Results](./etims-tracking-results.md).

## Environments (dev vs prod)

The collection variables default to the development setup. To switch to production, create a Postman **Environment** with a production `baseUrl` and your `sk_production_…` key, and select it before running.

## Read next

- [Get Started with eTIMS](./etims-getting-started.md) — the guided journey
- [API Reference](./etims-api-reference.md) — full field and enum reference
