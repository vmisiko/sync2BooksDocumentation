# Get started with Expenses

This guide will help you set up your Expenses integration and make your first expense sync.

## Overview

When implementing your Expenses solution, you need to:

1. **Create a company** - Represent your SMB customer in Sync2Books
2. **Create an accounting connection** - Connect to your customer's accounting software
3. **Configure expense mapping** - Set up default accounts, suppliers, and tax rates
4. **Create expense transactions** - Submit expenses for sync
5. **Monitor sync status** - Track the sync process and handle any errors

## Prerequisites

Before you begin, ensure you have:

- ✅ **API Key** - Your application's API key from the Sync2Books Dashboard
- ✅ **Access to accounting software** - Your customer's QuickBooks, Xero, or Sage account credentials

## Authorize your API calls

Remember to authenticate when making calls to our API. Navigate to **Applications** → Select your application in the [Sync2Books Dashboard](https://app.sync2books.com) to pick up your authorization header.

Your API key will look like: `sk_live_abc123...` or `sk_test_xyz789...`

**Example Authentication:**

```bash
curl -X GET "https://api.sync2books.com/v1/companies" \
  -H "X-API-Key: {apiKey}"
```

## Step 1: Create a company

Within Expenses, a company represents your SMB customer that manages their expenses using your application. To create it, use our Create company endpoint. It returns a JSON response containing the company `id`. You will use this `id` to establish a connection to an accounting software.

#### Request

```bash
POST /companies

{
    "name": "{companyName}"
}
```

#### Response

```json
{
  "company": {
    "id": "77921ff9-2491-4dfe-b23b-ff28f3e31e4f",
    "name": "Sawayn Group",
    "isActive": true
  },
  "authUrl": "https://appcenter.intuit.com/connect/oauth2?..."
}
```

## Step 2: Create accounting connection

Next, use the authorization URL returned when creating a company to connect the company to an accounting data source via one of our integrations. This will allow you to synchronize data with that source.

### QuickBooks Online

1. Open the `authUrl` from the company creation response in a browser
2. Complete the OAuth authorization flow with QuickBooks
3. After authorization, the connection is automatically created

You can also get the authorization URL for an existing company:

```bash
curl -X GET "https://api.sync2books.com/v1/companies/{companyId}/auth-url?integrationKey=QUICKBOOKS" \
  -H "X-API-Key: {apiKey}"
```

#### Response

```json
{
  "connections": [
    {
      "id": "7baba7cc-4ae0-48fd-a617-98d55a6fc008",
      "integrationKey": "QUICKBOOKS",
      "companyId": "77921ff9-2491-4dfe-b23b-ff28f3e31e4f",
      "status": "CONNECTED"
    }
  ]
}
```

## Step 3: Configure expense mapping (optional)

Before creating expenses, you can configure default mappings at the company level. This ensures expenses are automatically categorized correctly even if specific references are omitted.

#### Request

```bash
PATCH /companies/{companyId}/expense-config

{
  "bankAccount": {
    "id": "bank-account-id"
  },
  "supplier": {
    "id": "supplier-id"
  },
  "defaultAccount": {
    "id": "expense-account-id"
  },
  "defaultTaxRate": {
    "id": "tax-rate-id"
  }
}
```

See [Map transactions](./expenses-map-transactions.md) for detailed configuration options.

## Step 4: Create your first expense

Now that you have a company and connection set up, you can create expense transactions:

#### Request

```bash
POST /expenses/{connectionId}

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
      }
    }
  ],
  "notes": "Office supplies for Q1 2024",
  "postAsDraft": false
}
```

#### Response

```json
{
  "syncBatchId": "550e8400-e29b-41d4-a716-446655440000",
  "totalExpenses": 1
}
```

The response includes a `syncBatchId` that you can use to monitor the sync status.

## Step 5: Monitor sync status

Use the `syncBatchId` to monitor the sync progress:

#### Request

```bash
GET /sync/batches/{syncBatchId}
```

#### Response

```json
{
  "batch": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "companyId": "77921ff9-2491-4dfe-b23b-ff28f3e31e4f",
    "connectionId": "7baba7cc-4ae0-48fd-a617-98d55a6fc008",
    "status": "completed",
    "totalItems": 1,
    "successfulItems": 1,
    "failedItems": 0,
    "createdAt": "2024-01-15T10:00:00Z",
    "completedAt": "2024-01-15T10:00:05Z"
  },
  "items": [
    {
      "id": "item-uuid-1",
      "entityId": "expense-001",
      "entityType": "Expense",
      "status": "success",
      "integrationResponse": {
        "id": "qb-expense-id",
        "syncToken": "0"
      },
      "syncErrorMessage": null,
      "createdAt": "2024-01-15T10:00:00Z",
      "updatedAt": "2024-01-15T10:00:05Z"
    }
  ]
}
```

See [Sync transactions](./expenses-sync-transactions.md) for detailed status tracking and error handling.

## Recap

You have created the structure of key objects required by Sync2Books Expenses: a company and its connection to an accounting data source. You've also created and synced your first expense transaction.

## Read next

* [Configure customer](./expenses-configure-customer.md) - Learn how to set up companies and connections
* [Map transactions](./expenses-map-transactions.md) - Configure expense mapping preferences
* [Create transactions](./expenses-create-transactions.md) - Learn how to create expense transactions
* [Sync transactions](./expenses-sync-transactions.md) - Understand the sync process
* [Upload receipts](./expenses-upload-receipts.md) - Attach files to expenses
