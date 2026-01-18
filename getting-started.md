# Getting Started

This guide will help you set up your Sync2Books integration and make your first API call.

With Sync2Books, you can easily build integrated financial products for SMBs. Set up your customers by adding them as companies in Sync2Books. Then, establish authorized connections to your customers' accounting software using one of our integrations. Finally, sync and review the financial data relevant to your use case.

This guide is aimed at developers and non-developers alike. In a few easy steps, you will create a company, link it to an accounting platform, and sync your first expense.

## Prerequisites

You need an account and API key to follow this guide. Get in touch to discuss creating an account today.

## Developer Prerequisites

If you are a developer and want to work with Sync2Books using our API, you first need to authenticate.

**Authenticate with Sync2Books API**

Sync2Books uses API keys, passed in the `X-API-Key` header, to control access to the API. To get your API key:

1. Log in to your [Sync2Books Dashboard](https://app.sync2books.com)
2. Navigate to **Applications** → Select your application
3. Copy your **API Key** from the settings page

Your API key will look like: `sk_live_abc123...` or `sk_test_xyz789...`

Then, replace `{apiKey}` in the code snippets below.

**Example Authentication:**

```bash
curl -X GET "https://api.sync2books.com/v1/companies" \
  -H "X-API-Key: {apiKey}"
```

## Step 1: Create a Company

Set up your SMB customer by adding them as a company in Sync2Books. A company represents your customer's business entity and can have multiple connections to different accounting platforms.

**Create a company using Sync2Books API**

To create a company in Sync2Books, use the `POST /companies` endpoint with a request body containing the `name` of the company. It does not have to be unique and serves to identify your customer in Sync2Books.

```bash
curl -X POST "https://api.sync2books.com/v1/companies" \
  -H "X-API-Key: {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation"
  }'
```

**Response:**

```json
{
  "company": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Acme Corporation",
    "isActive": true
  },
  "authUrl": "https://appcenter.intuit.com/connect/oauth2?..."
}
```

The response includes:
- `company.id`: The unique identifier for your company (save this for later steps)
- `authUrl`: The authorization URL to connect the company to an accounting platform

## Step 2: Create a Connection

Before you can sync data, you need to connect an accounting system. The `authUrl` returned when creating a company is used to authorize the connection.

**Option A: Use the Link Component (Recommended)**

The Link component provides a pre-built UI for connecting accounting systems. See [Link Integration](./link-integration.md) for framework-specific guides.

**Option B: Direct Authorization URL**

1. Open the `authUrl` from the company creation response in a browser
2. Complete the OAuth authorization flow with the accounting platform (e.g., QuickBooks)
3. After authorization, the connection is automatically created

You can also get the authorization URL for an existing company:

```bash
curl -X GET "https://api.sync2books.com/v1/companies/{companyId}/auth-url?integrationKey=QUICKBOOKS" \
  -H "X-API-Key: {apiKey}"
```

**List connections for a company:**

```bash
curl -X GET "https://api.sync2books.com/v1/companies/{companyId}/connections" \
  -H "X-API-Key: {apiKey}"
```

**Response:**

```json
{
  "connections": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "integrationKey": "QUICKBOOKS",
      "companyId": "550e8400-e29b-41d4-a716-446655440000",
      "status": "CONNECTED"
    }
  ]
}
```

Save the `connectionId` from the response - you'll need it for syncing data.

## Step 3: Sync Your First Expense

Now that you have a company and connection set up, you can sync financial data. Let's create a simple expense:

```bash
curl -X POST "https://api.sync2books.com/v1/expenses/{connectionId}" \
  -H "X-API-Key: {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "expense-001",
    "type": "Payment",
    "issueDate": "2024-01-15T00:00:00Z",
    "currency": "USD",
    "currencyRate": 1,
    "merchantName": "Office Supplies Co",
    "lines": [
      {
        "netAmount": 100.00,
        "taxAmount": 10.00,
        "taxRateRef": {
          "id": "tax-rate-id"
        },
        "accountRef": {
          "id": "account-id"
        }
      }
    ]
  }'
```

**Response:**

```json
{
  "syncBatchId": "550e8400-e29b-41d4-a716-446655440000",
  "totalExpenses": 1
}
```

The response includes a `syncBatchId` that you can use to monitor the sync status.

## Step 4: Check Sync Status

Use the `syncBatchId` to monitor the sync progress:

```bash
curl -X GET "https://api.sync2books.com/v1/sync/batches/{syncBatchId}" \
  -H "X-API-Key: {apiKey}"
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "companyId": "550e8400-e29b-41d4-a716-446655440000",
  "connectionId": "660e8400-e29b-41d4-a716-446655440001",
  "status": "completed",
  "totalItems": 1,
  "successfulItems": 1,
  "failedItems": 0,
  "createdAt": "2024-01-15T10:00:00Z",
  "completedAt": "2024-01-15T10:00:05Z"
}
```

## Recap

You have now:

- created a Sync2Books company that represents your small business customer,
- authorized a connection to read financial data from an accounting platform, and
- synced your first expense and reviewed its status.

## Next Steps

#### Want to read and view data from a different platform?

Sync2Books enables you to connect to multiple accounting platforms including QuickBooks Online, QuickBooks Desktop, Xero, and Sage. Navigate to your application settings in the Dashboard to configure additional integrations.

#### Curious about what other data Sync2Books can sync?

Sync2Books can sync a variety of data types including expenses, customers, suppliers, bills, payments, and more. See our [API Reference](./api-reference.md) for a complete list of supported entities.

#### Want to customize the authorization flow?

Colors, logos, and branding of Sync2Books' authorization flow can be customized for a bespoke experience. Navigate to **Settings** → **Applications** → **Link Settings** in the Sync2Books Dashboard to adjust the flow to fit your brand.

## API Reference

### Base URL

- **Production**: `https://api.sync2books.com/v1`
- **Sandbox**: `https://sandbox-api.sync2books.com/v1` (coming soon)

### Rate Limits

- **Standard**: 100 requests per minute per API key
- **Burst**: Up to 200 requests per minute for short bursts

Rate limit headers are included in all responses:
- `X-RateLimit-Limit`: Maximum requests per window
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Unix timestamp when the limit resets

### Error Handling

All errors follow a consistent format:

```json
{
  "statusCode": 400,
  "message": "Validation failed",
  "error": "Bad Request"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid API key)
- `404` - Not Found
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

## Additional Resources

- **[Expense Management](./expense-management.md)** - Learn how to create and sync expenses
- **[Sync & Monitoring](./sync-and-monitoring.md)** - Track sync status and monitor operations
- **[Link Integration](./link-integration.md)** - Integrate the Link component in your application
- **[API Reference](./api-reference.md)** - Complete API documentation
