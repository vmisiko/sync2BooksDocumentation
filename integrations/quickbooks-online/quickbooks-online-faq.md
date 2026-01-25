# QuickBooks Online FAQs

Answers to common questions about the QuickBooks Online integration.

## General questions

### What QuickBooks Online versions are supported?

Sync2Books supports all current versions of QuickBooks Online, including:
- QuickBooks Online Simple Start
- QuickBooks Online Essentials
- QuickBooks Online Plus
- QuickBooks Online Advanced

### Do I need a QuickBooks Online subscription?

Yes, you need an active QuickBooks Online subscription to use the integration. You can use the QuickBooks Online sandbox for testing without a subscription.

### Can I connect multiple QuickBooks Online companies?

Yes, each company in Sync2Books can have its own QuickBooks Online connection. You can also connect multiple companies to the same QuickBooks Online account if needed.

## Authentication

### How does OAuth work with QuickBooks Online?

Sync2Books uses OAuth 2.0 to authenticate with QuickBooks Online. When you create a company and get an authorization URL, your customer completes the OAuth flow to grant access. Sync2Books handles token management automatically.

### How long do connections stay active?

Connections remain active as long as:
- The OAuth token hasn't expired
- The user hasn't revoked access in QuickBooks Online
- The connection hasn't been manually disconnected

### What happens if a connection expires?

If a connection expires, you'll need to reconnect the company. Sync2Books will attempt to refresh tokens automatically when possible.

## Expense transactions

### What expense types are supported?

- **Payment** - Standard expense payment
- **DirectCost** - Direct cost expense (COGS)
- **Reimbursable** - Billable to customers
- **Transfer** - Transfer between accounts
- **Adjustment** - Refunds, chargebacks, rewards

### Can I create draft expenses?

Yes, set `postAsDraft: true` when creating an expense. The expense will be created as a draft in QuickBooks Online and won't affect the books until posted.

### How are expenses categorized?

Expenses are categorized using:
- **Account reference** - Maps to QuickBooks Online chart of accounts
- **Tax rate reference** - Maps to QuickBooks Online tax rates
- **Tracking categories** - Maps to classes, locations, etc.

### Can I update expenses after they're synced?

Currently, Sync2Books creates expenses but doesn't support updates. To modify an expense, you'll need to do it directly in QuickBooks Online or create a new adjustment transaction.

## Attachments

### What file types are supported?

- **Images**: JPG, JPEG, PNG, GIF
- **Documents**: PDF, DOC, DOCX, XLS, XLSX, TXT, CSV
- **Max file size**: 10 MB

### Can I attach multiple files to one expense?

Yes, but you need to upload each file separately. Each upload creates a separate attachment record.

### Where do attachments appear in QuickBooks Online?

Attachments appear in QuickBooks Online as "Attachables" linked to the expense transaction. They're accessible from the transaction detail page.

## Sync process

### How long does syncing take?

Most expense syncs complete within 5-15 seconds. Large batches may take longer. Use the sync batch status endpoint to monitor progress.

### What happens if a sync fails?

Failed syncs are tracked in the sync batch. You can:
- Check the error message in the sync batch response
- Retry failed items using the retry endpoint
- Fix any data issues and resubmit

### Can I sync expenses in bulk?

Yes, you can create multiple expenses in a single request. They'll be processed as a batch and share the same sync batch ID.

## Rate limits

### What are the rate limits?

QuickBooks Online has rate limits based on your subscription tier. Sync2Books respects these limits and handles rate limit errors automatically with retries.

### What happens if I exceed rate limits?

If you exceed rate limits, Sync2Books will:
- Return a rate limit error
- Automatically retry after the rate limit window expires
- Queue requests if needed

## Troubleshooting

### Connection status shows ERROR

1. Check the connection details in Sync2Books Dashboard
2. Verify the OAuth token hasn't expired
3. Try reconnecting the company
4. Check QuickBooks Online for any account issues

### Expenses aren't syncing

1. Verify the connection is active (`status: "CONNECTED"`)
2. Check the sync batch status for error messages
3. Ensure all required fields are present (account, tax rate, etc.)
4. Verify account and tax rate IDs exist in QuickBooks Online

### Invalid account ID error

1. Retrieve accounts using the accounts endpoint
2. Verify the account ID exists in QuickBooks Online
3. Ensure the account is active
4. Check that the account type matches the expense type

### Invalid tax rate ID error

1. Retrieve tax rates using the tax rates endpoint
2. Verify the tax rate ID exists in QuickBooks Online
3. Ensure the tax rate is active
4. Check that the tax rate applies to the expense location

## Best practices

### How should I handle errors?

1. Always check sync batch status after creating expenses
2. Implement retry logic for transient failures
3. Log errors for debugging
4. Set up alerts for high failure rates

### Should I set company-level defaults?

Yes, setting company-level defaults reduces transaction complexity and ensures consistent categorization. See [Map transactions](../expenses-map-transactions.md) for details.

### How often should I sync expenses?

Sync expenses as they occur for real-time updates. Batch multiple expenses together for better efficiency.

## Support

### Where can I get help?

- Check the [QuickBooks Online integration reference](./quickbooks-online-reference.md)
- Review [Sync transactions](../expenses-sync-transactions.md) for sync troubleshooting
- Contact Sync2Books support for integration-specific issues

## Read next

* [QuickBooks Online overview](./quickbooks-online-overview.md) - Learn about the integration
* [Set up the QuickBooks Online integration](./quickbooks-online-setup.md) - Configuration guide
* [QuickBooks Online integration reference](./quickbooks-online-reference.md) - API reference
