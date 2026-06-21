# Codes & Values

Several catalog and sales fields take **codes**. This page lists the values Sync2Books recognizes so you can fill them in correctly for your items and packaging.

> **The good news:** most codes are resolved for you. You only ever *must* supply a **classification code** (and even that can be pre-configured for your account). Everything else has a sensible default or a simple enum.

> There is **no live lookup endpoint** yet — the tables below are the values the API accepts out of the box. For the complete, authoritative KRA lists (especially item classifications), use the [KRA references](#kra-references) at the bottom.

## Tax category

Send `taxCategory` (an enum) when registering an item and on each sale line. Sync2Books maps it to the correct KRA tax type automatically — you don't send a tax code yourself.

| `taxCategory` | KRA tax type | Meaning |
|---------------|--------------|---------|
| `VAT_STANDARD` | B | Standard-rated VAT (16%) |
| `VAT_ZERO` | C | Zero-rated (0%) |
| `EXEMPT` | A | Exempt |
| `OTHER` | D | Non-VAT / other |

> Need a special rate (e.g. VAT 8%) that the enum doesn't cover? Set the KRA tax type explicitly via `taxTyCd` on item register, or contact support.

## Item type & product type

`itemType` sets whether an item is stock-tracked (see [Goods vs Services](./etims-catalog.md#goods-vs-services-stock-vs-non-stock)) and selects the KRA product type:

| `itemType` | KRA product type | Stock-tracked |
|-----------|------------------|---------------|
| `GOODS` | `2` (Finished Product) | Yes |
| `SERVICE` | `3` (Service) | No |

To use a different KRA product type — e.g. **raw materials** — set `productTypeCode` explicitly on register:

| `productTypeCode` | Meaning |
|-------------------|---------|
| `1` | Raw Material |
| `2` | Finished Product |
| `3` | Service |

## Units & packaging

You have two options when registering an item:

**Option A — let Sync2Books resolve them.** Send `internalUnit` with one of these recognized values and the quantity/packaging codes are filled in for you:

| `internalUnit` | → `unitCode` | → `packagingUnitCode` |
|----------------|-------------|------------------------|
| `EA`, `EACH`, `PCS` | `U` | `NT` |
| `KG`, `KILOGRAM` | `KG` | `NT` |
| `L`, `LTR`, `LITRE` | `LTR` | `NT` |

**Option B — pass the KRA codes directly** via `unitCode` and `packagingUnitCode`:

Quantity unit (`unitCode`):

| Code | Meaning |
|------|---------|
| `U` | Pieces / item |
| `KG` | Kilo-gramme |
| `LTR` | Litre |

Packaging unit (`packagingUnitCode`):

| Code | Meaning |
|------|---------|
| `NT` | Net |
| `BL` | Bale |
| `BX` | Box |

> These are the common units recognized out of the box. KRA defines many more (per the TIS spec). If you need a unit not listed here, pass its KRA code directly in `unitCode` / `packagingUnitCode`.

## Payment type (sales)

Send `paymentTypeCode` when creating a sale:

| Code | Method |
|------|--------|
| `01` | Cash |
| `02` | Credit |
| `03` | Cash / Credit |
| `04` | Bank cheque |
| `05` | Debit & Credit |
| `06` | Card |
| `07` | Mobile money |
| `08` | Other |

## Classification code (the one you must look up)

`classificationCode` is the KRA **item classification** (`itemClsCd`) for the product — e.g. `14111400`. Unlike the other codes, **there is no default**: you must supply a valid code when registering an item, unless classification rules have been pre-configured for your account.

- Get valid codes from **KRA's item classification list** (see [references](#kra-references)).
- Pick the code that best matches the product.
- Once set, the item can be synced and sold.

If you register without it and no rule applies, the request is rejected with `Missing classification mapping`.

## Other sale codes

A sale also carries a couple of KRA status codes. Common values:

| Field | Common value | Notes |
|-------|--------------|-------|
| `receiptTypeCode` | `S` | Normal sale |
| `invoiceStatusCode` | `02` | Per KRA invoice/sale status codes |

These follow the KRA TIS code lists — use the [references](#kra-references) for the full set.

## KRA references

The authoritative, complete code lists are published by KRA:

- **[TIS for OSCU/VSCU Technical Specifications v2.0](https://kra.go.ke/images/publications/TIS-for-OSCU--VSCU-Technical-Specifications-v2.0.pdf)** — all code lists (tax types, units, packaging, product types, payment methods, receipt/invoice status) and the item classification structure.
- See also **[eTIMS as a Third-Party Integrator (OSCU)](./ETIMS_OSCU_INTEGRATION_AS_THIRD_PARTY.md)** for how these fit the KRA onboarding flow.

## Read next

- [Catalog](./etims-catalog.md) — register and sync items
- [Sales & Credit Notes](./etims-sales.md) — where payment/receipt codes are used
- [API Reference](./etims-api-reference.md) — full field reference
