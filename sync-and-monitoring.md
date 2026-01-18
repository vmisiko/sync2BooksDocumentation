# Sync & Monitoring

Learn how to track sync status, handle errors, and retry failed syncs.

## Overview

When you create an expense, bill, or invoice, Sync2Books automatically queues it for sync to your connected accounting system. This guide shows you how to monitor the sync process and handle any issues.

## Sync Lifecycle

```
┌─────────────┐
│ PENDING     │  ← Expense created, waiting to sync
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PROCESSING  │  ← Currently syncing to accounting system
└──────┬──────┘
       │
       ├─────────▶ ┌─────────────┐
       │          │ SUCCESS      │  ← Synced successfully
       │          └──────────────┘
       │
       └─────────▶ ┌─────────────┐
                  │ FAILED       │  ← Sync failed (can retry)
                  └──────────────┘
```

## Getting Sync Batch Status

After creating expenses, you receive a `syncBatchId`. Use this to check the sync status:

### Endpoint

```
GET /sync/batches/{syncBatchId}
```

### Request

```bash
curl -X GET "https://api.sync2books.com/v1/sync/batches/{syncBatchId}" \
  -H "X-API-Key: sk_live_your_api_key"
```

### Response

```json
{
  "batch": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "companyId": "company-uuid",
    "connectionId": "connection-uuid",
    "status": "completed",
    "totalItems": 2,
    "successfulItems": 2,
    "failedItems": 0,
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:31:00Z",
    "completedAt": "2024-01-15T10:31:00Z"
  },
  "items": [
    {
      "id": "item-uuid-1",
      "entityId": "expense-uuid-1",
      "entityType": "Expense",
      "status": "success",
      "integrationResponse": {
        "id": "qb-expense-id",
        "syncToken": "0"
      },
      "syncErrorMessage": null,
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-01-15T10:31:00Z"
    },
    {
      "id": "item-uuid-2",
      "entityId": "expense-uuid-2",
      "entityType": "Expense",
      "status": "success",
      "integrationResponse": {
        "id": "qb-expense-id-2",
        "syncToken": "0"
      },
      "syncErrorMessage": null,
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-01-15T10:31:00Z"
    }
  ]
}
```

### Batch Status Values

| Status | Description |
|--------|-------------|
| `pending` | Batch is queued, waiting to be processed |
| `processing` | Currently syncing items to accounting system |
| `completed` | All items processed (may include failures) |
| `failed` | Batch processing failed entirely |

### Item Status Values

| Status | Description |
|--------|-------------|
| `pending` | Item is queued |
| `processing` | Currently syncing |
| `success` | Successfully synced to accounting system |
| `failed` | Sync failed (can retry) |

## Listing Sync Batches

### Get All Batches for a Company

```
GET /sync/companies/{companyId}/batches
```

### Query Parameters

- `page` (number, default: 1) - Page number
- `limit` (number, default: 20) - Items per page
- `status` (string, optional) - Filter by status: `pending`, `processing`, `completed`, `failed`
- `startDate` (string, optional) - Filter batches from this date (ISO 8601)
- `endDate` (string, optional) - Filter batches until this date (ISO 8601)

### Example

```bash
curl -X GET "https://api.sync2books.com/v1/sync/companies/{companyId}/batches?page=1&limit=20&status=completed" \
  -H "X-API-Key: sk_live_your_api_key"
```

### Response

```json
{
  "batches": [
    {
      "id": "batch-uuid-1",
      "status": "completed",
      "totalItems": 5,
      "successfulItems": 5,
      "failedItems": 0,
      "createdAt": "2024-01-15T10:30:00Z",
      "completedAt": "2024-01-15T10:31:00Z"
    },
    {
      "id": "batch-uuid-2",
      "status": "completed",
      "totalItems": 3,
      "successfulItems": 2,
      "failedItems": 1,
      "createdAt": "2024-01-14T09:00:00Z",
      "completedAt": "2024-01-14T09:01:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 2,
    "totalPages": 1
  }
}
```

## Handling Failed Syncs

### Get Failed Items

```
GET /sync/batches/{syncBatchId}/failed-items
```

### Example

```bash
curl -X GET "https://api.sync2books.com/v1/sync/batches/{syncBatchId}/failed-items" \
  -H "X-API-Key: sk_live_your_api_key"
```

### Response

```json
{
  "items": [
    {
      "id": "item-uuid",
      "entityId": "expense-uuid",
      "entityType": "Expense",
      "status": "failed",
      "syncErrorMessage": "Invalid account ID: account-xyz does not exist",
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-01-15T10:31:00Z"
    }
  ]
}
```

### Retry Failed Items

```
POST /sync/batches/{syncBatchId}/retry
```

### Request Body

```json
{
  "itemIds": ["item-uuid-1", "item-uuid-2"]
}
```

If `itemIds` is empty or omitted, all failed items will be retried.

### Example

```bash
curl -X POST "https://api.sync2books.com/v1/sync/batches/{syncBatchId}/retry" \
  -H "X-API-Key: sk_live_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "itemIds": ["item-uuid-1"]
  }'
```

### Response

```json
{
  "retriedItems": 1,
  "newBatchId": "new-batch-uuid"
}
```

## Polling Strategy

For real-time status updates, poll the sync batch status:

### Recommended Approach

1. **Initial Poll**: Wait 2 seconds after creating expense
2. **Poll Interval**: Check every 2-3 seconds
3. **Timeout**: Stop polling after 60 seconds (syncs typically complete in 5-15 seconds)
4. **Exponential Backoff**: If status is `processing`, increase interval slightly

### Example Implementation (JavaScript)

```javascript
async function pollSyncStatus(syncBatchId, apiKey, timeoutMs = 60000) {
  const startTime = Date.now();
  const pollInterval = 2000; // 2 seconds

  while (Date.now() - startTime < timeoutMs) {
    const response = await fetch(
      `https://api.sync2books.com/v1/sync/batches/${syncBatchId}`,
      {
        headers: { 'X-API-Key': apiKey }
      }
    );
    
    const data = await response.json();
    
    if (data.batch.status === 'completed') {
      return data;
    }
    
    if (data.batch.status === 'failed') {
      throw new Error('Sync batch failed');
    }
    
    // Wait before next poll
    await new Promise(resolve => setTimeout(resolve, pollInterval));
  }
  
  throw new Error('Sync status polling timeout');
}
```

## Webhooks (Coming Soon)

Instead of polling, you can configure webhooks to receive real-time notifications when syncs complete. Contact support for early access.

## Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `Invalid account ID` | Account doesn't exist in accounting system | Verify account ID or create account first |
| `Invalid tax rate ID` | Tax rate doesn't exist | Verify tax rate ID or create tax rate first |
| `Connection expired` | OAuth token expired | Reconnect the accounting system via Link |
| `Rate limit exceeded` | Too many requests to accounting system | Wait and retry with exponential backoff |
| `Validation error` | Invalid data format | Check request body against API schema |

## Best Practices

1. **Always check sync status** - Don't assume syncs succeed immediately
2. **Implement retry logic** - Handle transient failures gracefully
3. **Log sync errors** - Track failed syncs for debugging
4. **Monitor batch completion** - Set up alerts for high failure rates
5. **Use webhooks when available** - More efficient than polling

## Next Steps

- **[Expense Management](./expense-management.md)** - Create and sync expenses
- **[Attachments](./attachments.md)** - Upload files to synced transactions
- **[Link Integration](./link-integration.md)** - Connect accounting systems
