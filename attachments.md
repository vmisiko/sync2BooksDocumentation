# Attachments

Learn how to upload files (receipts, invoices, documents) to synced transactions.

## Overview

Attachments allow you to link files to expenses, bills, invoices, and other transactions that have been synced to your accounting system. This is useful for:

- **Receipts** - Attach receipt images to expenses
- **Invoices** - Link invoice PDFs to bills
- **Supporting Documents** - Add contracts, agreements, or other files

## Prerequisites

Before uploading an attachment, ensure:

- ✅ The transaction has been **synced successfully** to the accounting system
- ✅ You have the **`syncId`** and **`transactionId`** from the sync response
- ✅ The file is in a supported format (see below)

## Supported File Types

- **Images**: JPG, JPEG, PNG, GIF
- **Documents**: PDF, DOC, DOCX, XLS, XLSX, TXT, CSV
- **Max File Size**: 10 MB

## Uploading an Attachment

### Endpoint

```
POST /connections/{connectionId}/syncs/{syncId}/transactions/{transactionId}/attachments
```

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `connectionId` | string (UUID) | The connection ID for the accounting system |
| `syncId` | string (UUID) | The sync batch ID from when you created the transaction |
| `transactionId` | string (UUID) | The transaction ID (expense ID, bill ID, etc.) |

### Request

The request must be sent as `multipart/form-data`:

```bash
curl -X POST \
  "https://api.sync2books.com/v1/connections/{connectionId}/syncs/{syncId}/transactions/{transactionId}/attachments" \
  -H "X-API-Key: sk_live_your_api_key" \
  -F "file=@/path/to/receipt.jpg" \
  -F "note=Receipt for office supplies" \
  -F "includeOnSend=false"
```

### Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file (binary) | ✅ | The file to upload |
| `note` | string | ❌ | Optional note/description for the attachment |
| `includeOnSend` | boolean | ❌ | If `true`, attachment is included when sending the transaction via email (default: `false`) |
| `lineInfo` | string | ❌ | For line-item specific attachments (advanced) |

### Example: Upload Receipt to Expense

```bash
# Step 1: Create expense and get syncId
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
    "lines": [...]
  }'

# Response: { "syncBatchId": "sync-uuid", "totalExpenses": 1 }

# Step 2: Wait for sync to complete (check status)
curl -X GET "https://api.sync2books.com/v1/sync/batches/sync-uuid" \
  -H "X-API-Key: sk_live_your_api_key"

# Step 3: Upload attachment using syncId and transactionId (expense ID)
curl -X POST \
  "https://api.sync2books.com/v1/connections/{connectionId}/syncs/sync-uuid/transactions/exp-001/attachments" \
  -H "X-API-Key: sk_live_your_api_key" \
  -F "file=@receipt.jpg" \
  -F "note=Amazon receipt for office supplies"
```

### Example: JavaScript/TypeScript

```typescript
async function uploadAttachment(
  connectionId: string,
  syncId: string,
  transactionId: string,
  file: File,
  apiKey: string
) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('note', 'Receipt for office supplies');
  formData.append('includeOnSend', 'false');

  const response = await fetch(
    `https://api.sync2books.com/v1/connections/${connectionId}/syncs/${syncId}/transactions/${transactionId}/attachments`,
    {
      method: 'POST',
      headers: {
        'X-API-Key': apiKey,
      },
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`);
  }

  return await response.json();
}

// Usage
const fileInput = document.querySelector('input[type="file"]');
const file = fileInput.files[0];

await uploadAttachment(
  'connection-uuid',
  'sync-uuid',
  'expense-uuid',
  file,
  'sk_live_your_api_key'
);
```

### Example: Python

```python
import requests

def upload_attachment(connection_id, sync_id, transaction_id, file_path, api_key):
    url = f"https://api.sync2books.com/v1/connections/{connection_id}/syncs/{sync_id}/transactions/{transaction_id}/attachments"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'note': 'Receipt for office supplies',
            'includeOnSend': 'false'
        }
        headers = {'X-API-Key': api_key}
        
        response = requests.post(url, files=files, data=data, headers=headers)
        response.raise_for_status()
        return response.json()

# Usage
result = upload_attachment(
    'connection-uuid',
    'sync-uuid',
    'expense-uuid',
    '/path/to/receipt.jpg',
    'sk_live_your_api_key'
)
```

## Response

### Success Response (201 Created)

```json
{
  "id": "attachment-uuid",
  "fileName": "receipt.jpg",
  "contentType": "image/jpeg",
  "size": 245678,
  "category": "Expense",
  "note": "Receipt for office supplies",
  "includeOnSend": false,
  "connectionId": "connection-uuid",
  "syncId": "sync-uuid",
  "transactionId": "expense-uuid",
  "entityBookId": "qb-attachment-id",
  "createdAt": "2024-01-15T10:35:00Z"
}
```

### Error Responses

#### 400 Bad Request

```json
{
  "statusCode": 400,
  "message": "File is required",
  "error": "Bad Request"
}
```

#### 404 Not Found

```json
{
  "statusCode": 404,
  "message": "Sync batch or transaction not found",
  "error": "Not Found"
}
```

#### 413 Payload Too Large

```json
{
  "statusCode": 413,
  "message": "File size exceeds maximum of 10MB",
  "error": "Payload Too Large"
}
```

## Getting Transaction IDs

After creating an expense, bill, or invoice, you'll receive a `syncBatchId`. Use this to get the transaction details:

```bash
curl -X GET "https://api.sync2books.com/v1/sync/batches/{syncBatchId}" \
  -H "X-API-Key: sk_live_your_api_key"
```

The response includes sync items with `entityId` (your transaction ID) and `integrationResponse` (accounting system ID).

## Attachment Categories

Attachments are automatically categorized based on the transaction type:

- **`Expense`** - Attached to expenses
- **`Bill`** - Attached to bills
- **`Invoice`** - Attached to invoices
- **`Quote`** - Attached to quotes

## Best Practices

1. **Wait for sync completion** - Only upload attachments after the transaction has synced successfully
2. **Use appropriate file sizes** - Compress images before uploading
3. **Include descriptive notes** - Help users understand what the attachment is
4. **Handle errors gracefully** - Implement retry logic for network failures
5. **Validate file types** - Check file type before uploading

## Limitations

- **Max file size**: 10 MB per file
- **Supported formats**: Images (JPG, PNG, GIF) and documents (PDF, DOC, DOCX, XLS, XLSX, TXT, CSV)
- **One file per request**: Upload multiple files with separate requests
- **Transaction must be synced**: Cannot attach to pending transactions

## Next Steps

- **[Expense Management](./expense-management.md)** - Create and sync expenses
- **[Sync & Monitoring](./sync-and-monitoring.md)** - Track sync status
- **[Link Integration](./link-integration.md)** - Connect accounting systems
