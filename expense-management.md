# Expense Management

This guide covers how to create, sync, and manage expenses in Sync2Books.

## Overview

The expense management flow consists of three main steps:

1. **Create Expense** - Submit expense data to Sync2Books
2. **Automatic Sync** - Sync2Books automatically syncs to the connected accounting system
3. **Monitor Status** - Track sync progress and handle any errors

## Core Flow

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│ Your App   │─────▶│ Sync2Books   │─────▶│ Accounting      │
│            │      │ API          │      │ System (QBO)    │
└─────────────┘      └──────────────┘      └─────────────────┘
     │                      │                       │
     │ 1. POST /expenses    │                       │
     │─────────────────────▶│                       │
     │                      │                       │
     │ 2. syncBatchId       │                       │
     │◀─────────────────────│                       │
     │                      │                       │
     │                      │ 3. Sync to QBO         │
     │                      │──────────────────────▶│
     │                      │                       │
     │ 4. GET /sync/batches │                       │
     │─────────────────────▶│                       │
     │                      │                       │
     │ 5. Status response   │                       │
     │◀─────────────────────│                       │
```

## Prerequisites

Before creating expenses, ensure you have:

- ✅ **API Key** - Your application's API key
- ✅ **Connection ID** - A connected accounting system (QuickBooks, Xero, or Sage)
- ✅ **Account IDs** - Valid account IDs from the accounting system
- ✅ **Tax Rate IDs** - Valid tax rate IDs (if applicable)

## Creating an Expense

### Endpoint

```
POST /expenses/{connectionId}
```

### Request Body

```json
{
  "id": "expense-001",
  "type": "Payment",
  "issueDate": "2024-01-15T00:00:00Z",
  "currency": "USD",
  "currencyRate": 1,
  "merchantName": "Office Supplies Co",
  "contactRef": {
    "id": "supplier-id",
    "type": "Supplier"
  },
  "bankAccountRef": {
    "id": "bank-account-id"
  },
  "lines": [
    {
      "netAmount": 100.00,
      "taxAmount": 10.00,
      "taxRateRef": {
        "id": "tax-rate-id"
      },
      "accountRef": {
        "id": "expense-account-id"
      },
      "trackingRefs": [
        {
          "id": "tracking-category-id",
          "dataType": "trackingCategories"
        }
      ],
      "invoiceTo": {
        "id": "customer-id",
        "type": "Customer"
      }
    }
  ],
  "notes": "Office supplies for Q1 2024",
  "postAsDraft": false
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ | Unique identifier for the expense (UUID format recommended) |
| `type` | string | ✅ | Expense type: `"Payment"` or `"DirectCost"` |
| `issueDate` | string (ISO 8601) | ✅ | Date when the expense was incurred |
| `currency` | string | ✅ | Three-letter currency code (e.g., `"USD"`, `"GBP"`) |
| `currencyRate` | number | ✅ | Exchange rate (usually `1` for base currency) |
| `merchantName` | string | ✅ | Name of the merchant/vendor |
| `contactRef` | object | ❌ | Reference to a supplier/customer |
| `bankAccountRef` | object | ❌ | Reference to the bank account used |
| `lines` | array | ✅ | Array of expense line items |
| `notes` | string | ❌ | Additional notes about the expense |
| `postAsDraft` | boolean | ❌ | If `true`, creates as draft in accounting system |

### Expense Lines

Each expense line item requires:

- **`netAmount`** (number, required): Net amount before tax
- **`taxAmount`** (number, required): Tax amount
- **`taxRateRef`** (object, required): Reference to tax rate
- **`accountRef`** (object, required): Reference to expense account

Optional fields:

- **`trackingRefs`** (array): Tracking categories for reporting
- **`invoiceTo`** (object): Customer to invoice (for billable expenses)

### Example: Simple Expense

```bash
curl -X POST "https://api.sync2books.com/v1/expenses/{connectionId}" \
  -H "X-API-Key: sk_live_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "exp-001",
    "type": "Payment",
    "issueDate": "2024-01-15T00:00:00Z",
    "currency": "USD",
    "currencyRate": 1,
    "merchantName": "Amazon",
    "lines": [
      {
        "netAmount": 50.00,
        "taxAmount": 5.00,
        "taxRateRef": { "id": "tax-10-percent" },
        "accountRef": { "id": "office-supplies-account" }
      }
    ]
  }'
```

### Example: Multiple Expenses (Batch)

You can create multiple expenses in a single request:

```bash
curl -X POST "https://api.sync2books.com/v1/expenses/{connectionId}" \
  -H "X-API-Key: sk_live_your_api_key" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "id": "exp-001",
      "type": "Payment",
      "issueDate": "2024-01-15T00:00:00Z",
      "currency": "USD",
      "currencyRate": 1,
      "merchantName": "Amazon",
      "lines": [...]
    },
    {
      "id": "exp-002",
      "type": "Payment",
      "issueDate": "2024-01-16T00:00:00Z",
      "currency": "USD",
      "currencyRate": 1,
      "merchantName": "Staples",
      "lines": [...]
    }
  ]'
```

### Response

```json
{
  "syncBatchId": "550e8400-e29b-41d4-a716-446655440000",
  "totalExpenses": 1
}
```

The `syncBatchId` is used to track the sync status.

## Data Model

### Expense Entity

```typescript
{
  id: string;                    // Unique identifier
  type: "Payment" | "DirectCost";
  issueDate: string;              // ISO 8601 date
  currency: string;               // Currency code
  currencyRate: number;
  merchantName: string;
  contactRef?: {
    id: string;
    type: "Supplier" | "Customer";
  };
  bankAccountRef?: {
    id: string;
  };
  lines: ExpenseLine[];
  notes?: string;
  postAsDraft?: boolean;
}
```

### Expense Line

```typescript
{
  netAmount: number;
  taxAmount: number;
  taxRateRef: {
    id: string;
  };
  accountRef: {
    id: string;
  };
  trackingRefs?: Array<{
    id: string;
    dataType: "trackingCategories";
  }>;
  invoiceTo?: {
    id: string;
    type: "Customer";
  };
}
```

## Getting Account and Tax Rate IDs

Before creating expenses, you need valid IDs from your accounting system:

### QuickBooks Online

1. Use the QuickBooks API or UI to find:
   - **Account ID**: Chart of Accounts → Account → ID
   - **Tax Rate ID**: Tax Rates → Tax Rate → ID
   - **Supplier ID**: Vendors → Supplier → ID
   - **Customer ID**: Customers → Customer → ID

2. Or use Sync2Books reference endpoints (coming soon)

### Xero

Similar process using Xero's API or UI.

## Tracking Sync Status

After creating an expense, use the `syncBatchId` to monitor progress:

```bash
curl -X GET "https://api.sync2books.com/v1/sync/batches/{syncBatchId}" \
  -H "X-API-Key: sk_live_your_api_key"
```

See [Sync & Monitoring](./sync-and-monitoring.md) for detailed status tracking.

## Querying Expenses

### Get a Single Expense

```bash
curl -X GET "https://api.sync2books.com/v1/expenses/{expenseId}" \
  -H "X-API-Key: sk_live_your_api_key"
```

### Get Expenses by Connection

```bash
curl -X GET "https://api.sync2books.com/v1/expenses/connection/{connectionId}" \
  -H "X-API-Key: sk_live_your_api_key"
```

## Error Handling

### Validation Errors

If required fields are missing or invalid:

```json
{
  "statusCode": 400,
  "message": ["id should not be empty", "currency must be a string"],
  "error": "Bad Request"
}
```

### Sync Errors

If the sync fails, check the sync batch status for error details. See [Sync & Monitoring](./sync-and-monitoring.md) for error handling.

## Best Practices

1. **Use UUIDs for expense IDs** - Ensures uniqueness across your system
2. **Batch multiple expenses** - More efficient than individual requests
3. **Poll sync status** - Check every 2-3 seconds until complete
4. **Handle errors gracefully** - Implement retry logic for transient failures
5. **Validate data before sending** - Ensure all required fields are present

## Next Steps

- **[Sync & Monitoring](./sync-and-monitoring.md)** - Learn how to track sync status
- **[Attachments](./attachments.md)** - Upload files to expenses
- **[Link Integration](./link-integration.md)** - Connect accounting systems
