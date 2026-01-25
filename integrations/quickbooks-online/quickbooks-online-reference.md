# QuickBooks Online integration reference

Complete API reference for the QuickBooks Online integration.

## Overview

This reference covers the QuickBooks Online-specific endpoints and data types available through Sync2Books.

## Endpoints

### Accounts

#### Get accounts

Retrieve chart of accounts from QuickBooks Online.

```
GET /connections/{connectionId}/accounts
```

**Response:**

```json
{
  "accounts": [
    {
      "id": "64",
      "name": "Office Expenses",
      "type": "Expense",
      "subType": "OfficeExpenses",
      "status": "Active",
      "fullyQualifiedName": "Office Expenses"
    }
  ]
}
```

### Tax rates

#### Get tax rates

Retrieve tax rates from QuickBooks Online.

```
GET /connections/{connectionId}/tax-rates
```

**Response:**

```json
{
  "taxRates": [
    {
      "id": "tax-10",
      "name": "Sales Tax 10%",
      "rate": 10.0,
      "status": "Active"
    }
  ]
}
```

### Suppliers

#### Get suppliers

Retrieve vendors/suppliers from QuickBooks Online.

```
GET /connections/{connectionId}/suppliers
```

**Response:**

```json
{
  "suppliers": [
    {
      "id": "supplier-123",
      "name": "Office Supplies Co",
      "status": "Active"
    }
  ]
}
```

### Customers

#### Get customers

Retrieve customers from QuickBooks Online.

```
GET /connections/{connectionId}/customers
```

**Response:**

```json
{
  "customers": [
    {
      "id": "customer-456",
      "name": "Acme Corp",
      "status": "Active"
    }
  ]
}
```

### Tracking categories

#### Get tracking categories

Retrieve tracking categories (classes, locations, etc.) from QuickBooks Online.

```
GET /connections/{connectionId}/tracking-categories
```

**Response:**

```json
{
  "trackingCategories": [
    {
      "id": "class-1",
      "name": "Department",
      "options": [
        {
          "id": "option-1",
          "name": "Sales"
        },
        {
          "id": "option-2",
          "name": "Marketing"
        }
      ]
    }
  ]
}
```

## Data types

### Account

```typescript
{
  id: string;                    // QuickBooks account ID
  name: string;                 // Account name
  type: string;                 // Account type (e.g., "Expense")
  subType?: string;             // Account subtype
  status: "Active" | "Inactive";
  fullyQualifiedName: string;   // Fully qualified account name
}
```

### Tax rate

```typescript
{
  id: string;                   // QuickBooks tax rate ID
  name: string;                 // Tax rate name
  rate: number;                 // Tax rate percentage
  status: "Active" | "Inactive";
}
```

### Supplier

```typescript
{
  id: string;                   // QuickBooks vendor ID
  name: string;                 // Supplier name
  status: "Active" | "Inactive";
}
```

### Customer

```typescript
{
  id: string;                   // QuickBooks customer ID
  name: string;                 // Customer name
  status: "Active" | "Inactive";
}
```

### Tracking category

```typescript
{
  id: string;                   // QuickBooks tracking category ID
  name: string;                 // Category name
  options: Array<{
    id: string;                 // Option ID
    name: string;               // Option name
  }>;
}
```

## Expense transaction mapping

### QuickBooks Online expense structure

When syncing expenses to QuickBooks Online, they're mapped to QuickBooks Purchase transactions:

```json
{
  "Purchase": {
    "Id": "162",
    "SyncToken": "0",
    "TxnDate": "2024-01-15",
    "TotalAmt": 110.00,
    "PaymentType": "CreditCard",
    "AccountRef": {
      "value": "41",
      "name": "Checking Account"
    },
    "EntityRef": {
      "value": "supplier-123",
      "name": "Office Supplies Co"
    },
    "Line": [
      {
        "Amount": 110.00,
        "DetailType": "AccountBasedExpenseLineDetail",
        "AccountBasedExpenseLineDetail": {
          "AccountRef": {
            "value": "64",
            "name": "Office Expenses"
          },
          "TaxCodeRef": {
            "value": "tax-10"
          }
        }
      }
    ]
  }
}
```

## Supported operations

### Create expense

Creates a Purchase transaction in QuickBooks Online.

**Endpoint:** `POST /expenses/{connectionId}`

**QuickBooks mapping:**
- `merchantName` → `EntityRef.name`
- `bankAccountRef` → `AccountRef` (payment account)
- `lines[].accountRef` → `Line[].AccountBasedExpenseLineDetail.AccountRef`
- `lines[].taxRateRef` → `Line[].AccountBasedExpenseLineDetail.TaxCodeRef`

### Upload attachment

Creates an Attachable in QuickBooks Online linked to the expense.

**Endpoint:** `POST /connections/{connectionId}/syncs/{syncId}/transactions/{transactionId}/attachments`

**QuickBooks mapping:**
- File → `Attachable.AttachRef` linked to Purchase transaction

## Error codes

### QuickBooks-specific errors

| Error Code | Description | Solution |
|------------|-------------|----------|
| `3200` | Invalid account ID | Verify account exists and is active |
| `3201` | Invalid tax rate ID | Verify tax rate exists and is active |
| `3202` | Invalid vendor ID | Verify supplier exists and is active |
| `3203` | Invalid customer ID | Verify customer exists and is active |
| `3204` | Rate limit exceeded | Wait and retry with exponential backoff |
| `3205` | OAuth token expired | Reconnect the company |

## Rate limits

QuickBooks Online rate limits vary by subscription tier:

- **Simple Start**: 500 API calls per minute
- **Essentials**: 500 API calls per minute
- **Plus**: 500 API calls per minute
- **Advanced**: 500 API calls per minute

Sync2Books automatically handles rate limits and retries requests when needed.

## Best practices

1. **Cache reference data** - Store account, tax rate, and supplier IDs to reduce API calls
2. **Batch expenses** - Create multiple expenses in a single request
3. **Handle errors gracefully** - Implement retry logic for transient failures
4. **Monitor sync status** - Always check sync batch status after creating expenses
5. **Use company-level defaults** - Reduce transaction complexity

## Read next

* [QuickBooks Online overview](./quickbooks-online-overview.md) - Learn about the integration
* [Set up the QuickBooks Online integration](./quickbooks-online-setup.md) - Configuration guide
* [QuickBooks Online FAQs](./quickbooks-online-faq.md) - Common questions
