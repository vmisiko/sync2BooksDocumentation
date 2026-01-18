# Quick Start Guide

Get up and running with Sync2Books in 5 minutes.

## 1. Get Your API Key

1. Log in to [Sync2Books Dashboard](https://app.sync2books.com)
2. Go to **Applications** → Select your application
3. Copy your **API Key**

## 2. Connect QuickBooks

### Option A: Use Link Component (Recommended)

```tsx
import { useSync2Books } from '@sync2books/react';

function App() {
  const { openLink } = useSync2Books({
    companyId: 'your-company-id',
    applicationId: 'your-application-id',
    applicationName: 'My App',
    apiKey: 'sk_live_your_api_key',
    integrationKey: 'quickbooks',
    onSuccess: ({ connectionId }) => {
      console.log('Connected!', connectionId);
    },
  });

  return <button onClick={() => openLink()}>Connect QuickBooks</button>;
}
```

### Option B: Manual OAuth

Contact support for manual OAuth setup.

## 3. Create Your First Expense

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
        "netAmount": 100.00,
        "taxAmount": 10.00,
        "taxRateRef": { "id": "tax-rate-id" },
        "accountRef": { "id": "account-id" }
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

## 4. Check Sync Status

```bash
curl -X GET "https://api.sync2books.com/v1/sync/batches/{syncBatchId}" \
  -H "X-API-Key: sk_live_your_api_key"
```

## 5. Upload a Receipt (Optional)

```bash
curl -X POST \
  "https://api.sync2books.com/v1/connections/{connectionId}/syncs/{syncId}/transactions/{transactionId}/attachments" \
  -H "X-API-Key: sk_live_your_api_key" \
  -F "file=@receipt.jpg" \
  -F "note=Amazon receipt"
```

## That's It! 🎉

You've successfully:
- ✅ Connected QuickBooks
- ✅ Created an expense
- ✅ Synced it to QuickBooks
- ✅ Uploaded a receipt

## Next Steps

- **[Expense Management Guide](./expense-management.md)** - Learn more about creating expenses
- **[Sync & Monitoring](./sync-and-monitoring.md)** - Track sync status
- **[Link Integration](./link-integration.md)** - Integrate the Link component
- **[API Reference](./api-reference.md)** - Complete API documentation

## Need Help?

- **Email**: support@sync2books.com
- **Documentation**: This GitBook
- **Swagger UI**: [api.sync2books.com/docs](https://api.sync2books.com/docs)
