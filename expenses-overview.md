# Expenses

Write categorized expenses and attachments to all major accounting software, handling the complexities of expense reconciliation

## What is it?

**Expenses** is a standardized API-based solution that makes it easy to build and maintain accounting integrations and an end-to-end expense management process that customers love.

With **58% of small businesses** saying they choose one spending solution over another based on **quality of their accounting integrations**, Expenses enables you to write categorized expenses and attachments to your customers' accounting software via our high-quality accounting integrations.

It includes built-in logic so you can easily handle all of the complexities of expense reconciliation, such as refunds, accounting for multiple currencies, and allowing users to correct errors.

## Who is it for?

With Expenses, corporate card providers, expense management providers, and neobanks can easily embed accounting automation features in their solution that would otherwise take months or even years to design, build, and maintain from scratch.

## Why use it?

### Increase share of wallet

Make your card your customers' favorite way to spend through hassle-free accounting integrations that save them time on tedious financial admin.

### Go to market quickly

Ship robust expense management integrations with leading accounting software six times faster via our single, streamlined API.

### Free up development resources

Run your accounting integrations on our infrastructure proven at scale without the hassle of ongoing API maintenance and optimization.

### Get standardized data

Expenses is completely standardized with a data model based on the experience of expense card providers.

### Capture receipts

Easily upload receipts against an expense, providing your SMB customer with a full audit trail for each transaction.

### Two-way sync

Expenses stays in touch with the SMB customer's general ledger so that you can handle refunds, chargebacks, and other adjustments automatically.

## How it works

### Configure customer

Create a company and its connection that form the structure required to execute the expense sync process. Configure expense mapping preferences to associate expenses with correct accounts, suppliers, and customers.

### Map transactions

Associate expense transactions with the correct accounts, tax rates, suppliers, and customers in your customer's accounting software. Configure default mappings at the company level for automatic categorization.

### Create transactions

Create expense transactions in your system and submit them to Sync2Books. Expenses are queued for sync and processed asynchronously to your customer's accounting software.

### Sync transactions

The sync process processes the expenses you created, maps them into the format required by the accounting software, and records them in that platform. Syncs can be triggered manually or run automatically on a schedule.

### Upload attachments

When creating an expense transaction, allow your SMB customer to save a copy of the associated receipt in their accounting software.

## Supported integrations

| Integration | Status |
|------------|--------|
| QuickBooks Online | ✅ Supported |
| QuickBooks Desktop | ✅ Supported |
| Xero | ✅ Supported |
| Sage | ✅ Supported |

### Supported integrations by endpoint

| Integration | expense-transactions | reimbursable-expense-transactions | transfer-transactions | adjustment-transactions |
|------------|---------------------|----------------------------------|----------------------|------------------------|
| QuickBooks Online | ✔️ | ✔️ | ✔️ | ✔️ |
| QuickBooks Desktop | ✔️ | ✔️ | ✔️ | ✔️ |
| Xero | ✔️ | ✔️ | ✔️ | |
| Sage | ✔️ | ✔️ | | |

### Supported integrations by transaction type

| Integration | Payment | Refund | Reward | Chargeback |
|------------|---------|--------|--------|------------|
| QuickBooks Online | ✔️ | ✔️ | ✔️ | ✔️ |
| QuickBooks Desktop | ✔️ | ✔️ (credit card only) | ✔️ (credit card only) | ✔️ (credit card only) |
| Xero | ✔️ | ✔️ | ✔️ | ✔️ |
| Sage | ✔️ | ✔️ | | |

## Build with client libraries

Use our comprehensive SDKs to kick-start and simplify your developer journey automating the expense management process for your customers. The SDKs come in multiple languages and provide sample requests and responses for the full range of spend management scenarios.

### TypeScript/JavaScript

```bash
npm install @sync2books/sdk
```

### Python

```bash
pip install sync2books-sdk
```

### cURL

All examples in our documentation use cURL for maximum compatibility.

## Read next

* [Start building with the Expenses solution](./expenses-getting-started.md)
* [Configure customer](./expenses-configure-customer.md)
* [Map transactions](./expenses-map-transactions.md)
