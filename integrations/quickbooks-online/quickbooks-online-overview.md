# QuickBooks Online

Learn about our QuickBooks Online integration.

## Overview

You can synchronize accounting data with QuickBooks Online using our QuickBooks Online integration. This integration allows you to create expense transactions, sync them to QuickBooks Online, and manage attachments.

For more details about the supported data types and operations, see [QuickBooks Online integration reference](./quickbooks-online-reference.md).

## Set up the integration

See [Set up the QuickBooks Online integration](./quickbooks-online-setup.md) to learn how to set up and enable the integration.

## Supported operations

### Expense transactions

- ✅ Create expense payments
- ✅ Create direct cost expenses
- ✅ Create reimbursable expenses
- ✅ Create transfer transactions
- ✅ Create adjustment transactions (refunds, chargebacks, rewards)

### Transaction types

| Transaction Type | Supported |
|-----------------|-----------|
| Payment | ✔️ |
| Refund | ✔️ |
| Reward | ✔️ |
| Chargeback | ✔️ |

### Attachments

- ✅ Upload receipts and documents
- ✅ Link attachments to expense transactions
- ✅ Support for images (JPG, PNG, GIF) and documents (PDF, DOC, DOCX)

## Data types

### Accounts

Retrieve chart of accounts from QuickBooks Online to map expenses to the correct accounts.

### Tax rates

Retrieve tax rates from QuickBooks Online to apply correct tax calculations.

### Suppliers

Retrieve vendor/supplier information from QuickBooks Online.

### Customers

Retrieve customer information from QuickBooks Online for billable expenses.

### Tracking categories

Retrieve tracking categories (classes, locations, etc.) from QuickBooks Online for expense categorization.

## Authentication

QuickBooks Online uses OAuth 2.0 for authentication. When creating a company and connection, Sync2Books handles the OAuth flow automatically.

### Connection status

Connections can have the following statuses:

- **`CONNECTED`** - Connection is active and ready to sync
- **`DISCONNECTED`** - Connection was disconnected by the user
- **`ERROR`** - Connection has an error and needs attention

## Common use cases

### Expense management

Create expense transactions from card transactions and sync them to QuickBooks Online with proper categorization and tax handling.

### Receipt management

Upload receipts and attach them to expense transactions for a complete audit trail.

### Billable expenses

Mark expenses as billable to customers and track them for invoicing.

## FAQs

See [QuickBooks Online FAQs](./quickbooks-online-faq.md) for answers to common questions about the integration.

## Read next

* [Set up the QuickBooks Online integration](./quickbooks-online-setup.md) - Configure the integration
* [QuickBooks Online integration reference](./quickbooks-online-reference.md) - API reference
* [QuickBooks Online FAQs](./quickbooks-online-faq.md) - Common questions
