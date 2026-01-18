# API Reference

Complete API reference with interactive examples.

## Interactive API Documentation

For the complete, interactive API reference, visit our **Swagger UI**:

🔗 **[https://api.sync2books.com/docs](https://api.sync2books.com/docs)**

The Swagger UI provides:
- ✅ **Interactive testing** - Try API calls directly in your browser
- ✅ **Request/response examples** - See real examples for each endpoint
- ✅ **Schema definitions** - Understand request and response formats
- ✅ **Authentication** - Test with your API key

## Base URL

- **Production**: `https://api.sync2books.com/v1`
- **Sandbox**: `https://sandbox-api.sync2books.com/v1` (coming soon)

## Authentication

All API requests require authentication using the `X-API-Key` header:

```bash
curl -H "X-API-Key: sk_live_your_api_key_here" \
  https://api.sync2books.com/v1/...
```

## Endpoints Overview

### Expenses

- `POST /expenses/{connectionId}` - Create expense(s) and queue for sync
- `GET /expenses/{expenseId}` - Get a single expense
- `GET /expenses/connection/{connectionId}` - Get expenses by connection

### Sync

- `GET /sync/batches/{syncBatchId}` - Get sync batch status
- `GET /sync/companies/{companyId}/batches` - List sync batches for a company
- `POST /sync/batches/{syncBatchId}/retry` - Retry failed sync items
- `GET /sync/batches/{syncBatchId}/failed-items` - Get failed sync items

### Attachments

- `POST /connections/{connectionId}/syncs/{syncId}/transactions/{transactionId}/attachments` - Upload attachment

### Bills

- `POST /bills/{connectionId}` - Create bill(s) and queue for sync
- `GET /bills/{billId}` - Get a single bill

### Invoices

- `POST /invoices/{connectionId}` - Create invoice(s) and queue for sync
- `GET /invoices/{invoiceId}` - Get a single invoice

### Bill Payments

- `POST /bill-payments/{connectionId}` - Create bill payment(s) and queue for sync

## Rate Limits

- **Standard**: 100 requests per minute per API key
- **Burst**: Up to 200 requests per minute for short bursts

Rate limit headers:
- `X-RateLimit-Limit` - Maximum requests per window
- `X-RateLimit-Remaining` - Remaining requests in current window
- `X-RateLimit-Reset` - Unix timestamp when limit resets

## Error Codes

| Status Code | Description |
|-------------|-------------|
| `200` | Success |
| `201` | Created |
| `400` | Bad Request (validation error) |
| `401` | Unauthorized (invalid API key) |
| `404` | Not Found |
| `429` | Too Many Requests (rate limit exceeded) |
| `500` | Internal Server Error |

## Response Format

### Success Response

```json
{
  "data": { ... }
}
```

### Error Response

```json
{
  "statusCode": 400,
  "message": "Validation failed",
  "error": "Bad Request"
}
```

## SDKs and Libraries

- **[React](./link-integration.md#react-integration)** - `@sync2books/react`
- **[Vue](./link-integration.md#vue-integration)** - `@sync2books/vue`
- **[Angular](./link-integration.md#angular-integration)** - `@sync2books/angular` (coming soon)
- **[Svelte](./link-integration.md#svelte-integration)** - `@sync2books/svelte` (coming soon)

## Support

- **Email**: support@sync2books.com
- **Documentation**: This GitBook
- **Status Page**: [status.sync2books.com](https://status.sync2books.com)

---

**Ready to explore?** Visit the [Swagger UI](https://api.sync2books.com/docs) to try the API interactively.
