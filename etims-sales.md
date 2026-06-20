# Sales & Credit Notes

This is where compliance pays off: you submit a sale, the platform pushes it to KRA over OSCU, and KRA returns a **signed receipt (ETR number)**. You can then issue **credit notes** to reverse accepted sales.

## Prerequisites (read this first)

A sale will fail unless these are true. They are the most common stumbling blocks:

1. **The item is synced to eTIMS.** A registered-but-not-synced item is rejected with *"Item has not been synced to eTIMS"*. → [Catalog](./etims-catalog.md)
2. **For goods, there is enough stock.** Selling a **`GOODS`** item **deducts inventory**, so it fails with *"Insufficient stock"* if there isn't enough on hand — add stock first → [Stock](./etims-stock.md). **`SERVICE` items are non-stock**: skip this entirely; they can be sold right after syncing. See [Goods vs Services](./etims-catalog.md#goods-vs-services-stock-vs-non-stock).

So the working order is:

```
goods:    register → sync → add stock → create sale
services: register → sync →            create sale
```

## Create a sale

```bash
curl -X POST "https://api.sync2books.com/companies/{companyId}/integrations/etims/sales" \
  -H "X-API-Key: {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{
    "branchId": "HQ",
    "saleDate": "2026-06-20",
    "traderInvoiceNumber": "INV-0001",
    "receiptTypeCode": "S",
    "paymentTypeCode": "01",
    "invoiceStatusCode": "02",
    "customerName": "Walk-in",
    "items": [
      {
        "id": "{complianceItemId}",
        "quantity": 2,
        "unitPrice": 100,
        "taxCategory": "VAT_STANDARD",
        "taxAmount": 32,
        "itemDescription": "Maize Flour 2kg"
      }
    ]
  }'
```

```json
{ "syncBatchId": "e5f6…" }
```

This is **asynchronous** — you get a `syncBatchId` immediately; the receipt arrives once KRA accepts. See [Tracking Results](./etims-tracking-results.md).

### Request body

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `branchId` | string | ✅ | your branch key, e.g. `HQ` |
| `saleDate` | string | ✅ | `YYYY-MM-DD` |
| `traderInvoiceNumber` | string | ✅ | your invoice number |
| `receiptTypeCode` | string | ✅ | KRA receipt type, e.g. `S` (sale) |
| `paymentTypeCode` | string | ✅ | KRA payment type, e.g. `01` |
| `invoiceStatusCode` | string | ✅ | KRA invoice status, e.g. `02` |
| `customerTin`, `customerName` | string | — | buyer details |
| `items` | array | ✅ | at least one line |

For valid `receiptTypeCode`, `paymentTypeCode`, and `invoiceStatusCode` values, see **[Codes & Values](./etims-codes.md)**.

**Line item:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `id` | string | ✅ | the item `id` from Sync2Books (not your `externalId`) |
| `quantity` | number | ✅ | |
| `unitPrice` | number | ✅ | |
| `taxCategory` | string | ✅ | `VAT_STANDARD` \| `VAT_ZERO` \| `EXEMPT` \| `OTHER` |
| `taxAmount` | number | ✅ | tax for the line |
| `discountRate`, `discountAmount`, `itemDescription` | — | — | optional |

### The `submit` query flag

By default a sale is submitted to the OSCU pipeline. To persist a sale **without** submitting to KRA (e.g. staging a draft), pass `?submit=false`:

```
POST …/integrations/etims/sales?submit=false
```

## Sale outcome

A sale is processed asynchronously and ends in one of two outcomes:

- **Accepted** — KRA signed the invoice; the sale carries a KRA receipt number (e.g. `ETR-…`).
- **Rejected** — the submission failed; a human-readable reason is available.

Confirm the outcome via [List sales](#read-sales) or dashboard sync monitoring.

## Read sales

List sales (thin proxy to compliance):

```bash
curl -X GET "https://api.sync2books.com/companies/{companyId}/integrations/etims/sales?pageSize=20" \
  -H "X-API-Key: {apiKey}"
```

Query params: `before`, `after`, `startDate`, `endDate`, `pageSize` (all optional).

Get a single sale by its `id`:

```bash
curl -X GET "https://api.sync2books.com/companies/{companyId}/integrations/etims/sales/{saleId}" \
  -H "X-API-Key: {apiKey}"
```

## Express credit notes

To reverse an **accepted** sale, raise an express credit note referencing the sale's `id`:

```bash
curl -X POST "https://api.sync2books.com/companies/{companyId}/integrations/etims/sales/credit-notes/express" \
  -H "X-API-Key: {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{
    "branchId": "HQ",
    "saleId": "{saleDocumentId}",
    "traderInvoiceNumber": "CN-0001",
    "returnDate": "2026-06-20"
  }'
```

```json
{ "syncBatchId": "77aa…" }
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `branchId` | string | ✅ | |
| `saleId` | string | ✅ | the accepted sale's `id` |
| `traderInvoiceNumber` | string | ✅ | credit note number |
| `returnDate` | string | ✅ | `YYYY-MM-DD` |
| `paymentTypeCode`, `invoiceStatusCode` | string | — | optional overrides |

"Express" means the platform derives the credit note lines from the original sale, so you don't re-send line items. The result is a separate `CREDIT_NOTE` document. Like sales, it accepts `?submit=true|false`.

## Common errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Item has not been synced to eTIMS (missing etimsItemCode)` | Item registered but not synced | Run catalog sync → [Catalog](./etims-catalog.md) |
| `Insufficient stock: Have 0, tried to deduct N` | No inventory | Add stock → [Stock](./etims-stock.md) |
| Sale not accepted | A prerequisite failed | Check the failure reason → [Tracking Results](./etims-tracking-results.md) |
| Wrong line `id` | Used `externalId` instead of the item id | Use the item `id` from Sync2Books |

## Read next

- [Stock](./etims-stock.md) — keep inventory in sync
- [Tracking Results](./etims-tracking-results.md) — know when a sale is accepted
- [API Reference](./etims-api-reference.md#sales) — full field reference
