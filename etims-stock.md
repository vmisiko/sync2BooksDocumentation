# Stock (Inventory)

eTIMS tracks inventory movements. Sync2Books exposes two operations:

- **Adjust** — add or deduct stock for an item at a branch (`PUT …/stock/adjust`)
- **Transfer** — move stock between items/branches (`POST …/stock/transfer`)

> **Stock applies to goods only.** Only **`GOODS`** items are stock-tracked — for them, sales deduct inventory, so you must add stock before selling. **`SERVICE`** items are non-stock: these operations have no effect on them, and you never need to stock them to sell. See [Goods vs Services](./etims-catalog.md#goods-vs-services-stock-vs-non-stock).

Stock matters because, for goods, **sales deduct inventory** — you must add stock before a good can be sold. See [Sales prerequisites](./etims-sales.md#prerequisites-read-this-first).

## Adjust stock

> Note the HTTP method is **`PUT`**, not `POST`.

```bash
curl -X PUT "https://api.sync2books.com/companies/{companyId}/integrations/etims/stock/adjust" \
  -H "X-API-Key: {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{
    "itemId": "{itemId}",
    "branchId": "HQ",
    "quantity": 100,
    "action": "ADD"
  }'
```

```json
{ "syncBatchId": "c3d4…" }
```

### Request body

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `itemId` | string | ✅ | the item `id` from Sync2Books |
| `branchId` | string | ✅ | your branch key, e.g. `HQ` |
| `quantity` | number | ✅ | amount to add or deduct |
| `action` | `ADD` \| `DEDUCT` | ✅ | |
| `movementTypeCode` | string | — | KRA stock movement type override |
| `referenceId` | string | — | your own reference for traceability |

## Transfer stock

Move stock from one item/branch to another:

```bash
curl -X POST "https://api.sync2books.com/companies/{companyId}/integrations/etims/stock/transfer" \
  -H "X-API-Key: {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{
    "itemId": "{fromItemId}",
    "fromBranchId": "HQ",
    "receivingItemId": "{toItemId}",
    "toBranchId": "BR-01",
    "quantity": 5
  }'
```

```json
{ "syncBatchId": "88bb…" }
```

### Request body

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `itemId` | string | ✅ | source item `id` |
| `fromBranchId` | string | ✅ | source branch key |
| `receivingItemId` | string | ✅ | destination item `id` |
| `toBranchId` | string | ✅ | destination branch key |
| `quantity` | number | ✅ | |
| `referenceId` | string | — | your reference |

## Both are asynchronous

Adjust and transfer return a `syncBatchId` and are processed asynchronously — track them the same way as everything else: [Tracking Results](./etims-tracking-results.md).

## Typical pattern

```
add stock      → PUT  …/stock/adjust   { action: "ADD",    quantity: 100 }
sell           → POST …/sales          (deducts inventory)
correct count  → PUT  …/stock/adjust   { action: "DEDUCT", quantity: 3 }
move branches  → POST …/stock/transfer { fromBranchId, toBranchId }
```

## Read next

- [Sales & Credit Notes](./etims-sales.md) — sales consume the stock you add here
- [API Reference](./etims-api-reference.md#stock) — full field reference
