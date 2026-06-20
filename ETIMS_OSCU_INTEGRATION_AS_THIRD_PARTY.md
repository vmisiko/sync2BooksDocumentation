# eTIMS Integration as a Third-Party Integrator (OSCU Path)

This guide explains how **you** act as the third-party integrator: your platform syncs data between your customers’ accounting tools (e.g. QuickBooks, Xero) and KRA eTIMS via **OSCU** (or VSCU).

**References you have:**

- [TIS for OSCU/VSCU Technical Specifications v2.0](https://kra.go.ke/images/publications/TIS-for-OSCU--VSCU-Technical-Specifications-v2.0.pdf) – API contracts, request/response, data formats.
- [OSCU/VSCU Step-by-Step Guide](https://www.kra.go.ke/images/publications/OSCU_VSCU_Step-by-Step_Guide-on-how-to-sign-up.pdf) – Sign-up, approval, initialization, and process order.

---

## 0. Integration Token Is Required (OSCU and VSCU)

**If the eTIMS portal requires an Integration Token to submit a Service Request for both OSCU and VSCU**, you cannot complete the form without it. The token is **not** something you create yourself—it is **issued by KRA** after you become a **certified integrator**.

### How to get your Integration Tokenhttps://www.kra.go.ke/images/publications/OSCU_VSCU_Step-by-Step_Guide-on-how-to-sign-up.pdf

1. **Apply for certification with KRA**  
   You must be certified before you (or your customers) can use your token on the Service Request form.

   - **Official page:** [eTIMS System to System Integration - KRA](https://www.kra.go.ke/business/etims-electronic-tax-invoice-management-system/learn-about-etims/etims-system-to-system-integration)  
   - **Process:** Development → Testing (sandbox) → Vetting → **Certification**.  
   - **Who can apply:** Taxpayers who **self-integrate** or **third-party software developers (integrators)** who integrate on behalf of others. Both must be certified before going live.

2. **Submit the eTIMS Bio Data Form**  
   This is the formal application for certification.

   - **Form:** [eTIMS Bio Data Form for OSCU and VSCU](https://www.kra.go.ke/images/publications/eTIMS-Bio-Data-Form-for-OSCU-and-VSCU.pdf)  
   - **Submit to:** KRA eTIMS Operations (contact details on the form or via [eTIMS Contact and Support](https://www.kra.go.ke/business/etims-electronic-tax-invoice-management-system/learn-about-etims/etims-contact-and-support-details); support email: **timsupport@kra.go.ke**).

3. **What the Bio Data Form typically requires**
   - Company/business name, TCC (Tax Compliance Certificate).
   - Product description (your TIS / integration software).
   - Details of at least three qualified technical staff (CVs, terms of employment).
   - Read-only optical disk (or as specified) with your TIS integration software and documentation.  
   **For third-party vendors only:** Business registration (e.g. CR12), business permit, ID copies of directors/partners, experience in similar software, notarized declaration (e.g. not insolvent/receivership).

4. **After KRA approves your certification**  
   KRA will issue your **Integration Token**. You (and your customers, when they choose you as integrator) then use this token in the **Integration Token** field on the Service Request form and click **Verify** to proceed.

5. **Sandbox vs production**  
   Ask KRA eTIMS Operations explicitly: *“We are applying as a third-party integrator. The portal requires an Integration Token to submit a Service Request. How do we obtain the Integration Token for sandbox testing and for production?”* They may give you a sandbox token first so you can test before full production certification.

### 0.1 Development keys: what to use to build and demonstrate before KRA gives you the customer token

**There are no public "developer" or "test" Integration Tokens published by KRA.** The specs and step-by-step guide do not include a shared sandbox token. To develop first and show KRA your integration before you have the final token that customers will use, you must **get development/sandbox access from KRA**.

**What to do:**

1. **Contact KRA eTIMS and request a sandbox/development Integration Token**
   - **Email:** **timsupport@kra.go.ke**
   - **Phone:** +254 (0711) 099 999
   - **Page:** [eTIMS Contact and Support Details](https://www.kra.go.ke/business/etims-electronic-tax-invoice-management-system/learn-about-etims/etims-contact-and-support-details)

   Ask clearly, for example: *"We are applying to become a certified third-party integrator for eTIMS (OSCU/VSCU). To develop and test our integration we need to submit a Service Request on the sandbox portal, but the form requires an Integration Token. Please advise how we can obtain a sandbox or development Integration Token so we can build, test, and demonstrate our integration to KRA before full certification and before receiving the production token for our customers."*

2. **Possible outcomes (KRA will confirm)**  
   They may issue a provisional/sandbox-only token, or ask you to submit the Bio Data Form first and then provide a sandbox token as part of certification. Follow whatever KRA eTIMS Operations instructs.

3. **What you can do without a token (while waiting)**  
   Implement against the [Technical Spec v2.0](https://kra.go.ke/images/publications/TIS-for-OSCU--VSCU-Technical-Specifications-v2.0.pdf) (request/response formats, sequence, error handling), point your client at `https://etims-api-sbx.kra.go.ke` with placeholder credentials, prepare the Bio Data Form and supporting docs, and document your integration for KRA.

**Summary (Section 0):** For both OSCU and VSCU, if the portal mandates the Integration Token, the only way to get it is to **apply for certification** using the [eTIMS Bio Data Form](https://www.kra.go.ke/images/publications/eTIMS-Bio-Data-Form-for-OSCU-and-VSCU.pdf). To get **development keys** to build and demonstrate **before** the final customer token, **contact timsupport@kra.go.ke** and ask for a sandbox/development Integration Token or the process for the certification development phase.

---

## 1. OSCU vs VSCU (Why OSCU for You)

| | **OSCU** | **VSCU** |
|---|----------|----------|
| **Where it runs** | Hosted at **KRA**. Your backend calls KRA’s API. | Either KRA’s VSCU JAR on **client** side, or a certified provider. |
| **Integration Token** | **Required by portal.** You get **your own** token from KRA after **certification** (Bio Data Form). You use it when submitting Service Requests (your own or your customers’). | Same: you get your token from KRA after certification. Taxpayers entering your token on the form are choosing you as their integrator. |
| **Your role** | You build the **TIS (Trader Invoicing System)** that talks to **KRA’s OSCU API**. Each of your customers has their own KRA PIN, branch, and communication key; your API calls KRA on their behalf. | To “be” the third party in the same way, you’d need to be a **certified VSCU provider** and get your own token from KRA to give to taxpayers. |
| **Best fit for you** | **Yes.** Direct API integration, no dependency on another integrator. | Only if you later pursue certification as a VSCU provider. |

**Conclusion:** Use the **OSCU** path. Your system is the TIS; KRA’s OSCU is at `https://etims-api-sbx.kra.go.ke` (sandbox) and `https://etims-api.kra.go.ke` (production).

---

## 2. High-Level Flow (You as Integrator)

```
┌─────────────────┐     ┌──────────────────────────┐     ┌─────────────────┐
│  Your customer  │     │  Your platform (TIS)     │     │  KRA eTIMS      │
│  (Business)     │     │  - Stores credentials    │     │  OSCU API        │
│  - Accounting   │────▶│  - Syncs invoices,     │────▶│  - Validates    │
│    tool         │     │    items, stock, etc.   │     │  - Signs ETR    │
└─────────────────┘     └──────────────────────────┘     └─────────────────┘
```

1. **Customer onboarding**
   - Customer (or you on their behalf) signs up on eTIMS sandbox/production and submits a **Service Request for OSCU** (not VSCU).
   - After approval, they (or you) run **device initialization** with PIN, branch office ID, and equipment info → KRA returns a **communication key**.
   - You store **per connection**: KRA PIN, branch office ID, communication key (and any serial/cert the spec requires). No “Integration Token” is involved.

2. **Your API**
   - For each customer you call KRA’s OSCU endpoints with **their** credentials.
   - You implement the **mandatory sequence** (initialization → basic data → branch → items → sales/stock/purchases) as in the step-by-step guide.

3. **Two-way sync**
   - **To eTIMS:** Send sales, invoices, credit notes, items, stock in/out (from accounting tool → your API → KRA).
   - **From eTIMS:** Get purchases, item list, PIN list, notices, etc. (KRA → your API → accounting tool).

---

## 3. Where Credentials Come From (No Integration Token)

- **KRA PIN** – The business’s existing KRA PIN (used for eTIMS sign-up).
- **Branch office ID** – From KRA after OSCU approval (often `00` for first branch, then `01`, `02`…; exact values in portal or step-by-step guide).
- **Serial / equipment info** – As per the Technical Spec: either provided in the Service Request or assigned by KRA; used in the initialization call.
- **Communication key** – **Returned by KRA** when you call the **initialization** endpoint (`/selectInitOsdcInfo` or as in the spec). You must store it and use it for subsequent authenticated calls.

If the portal requires an **Integration Token** for both OSCU and VSCU, you must **first become a certified integrator** (Section 0). KRA issues your token after you submit the eTIMS Bio Data Form and are approved. Once you have the token, you (or your customers) use it on the Service Request form to get the request approved; **then** you use PIN, branch office ID, and the **communication key** from the initialization API for actual API calls.

---

## 4. Mandatory Order of Operations (From the Step-by-Step Guide)

The [OSCU/VSCU Step-by-Step Guide](https://www.kra.go.ke/images/publications/OSCU_VSCU_Step-by-Step_Guide-on-how-to-sign-up.pdf) and the Technical Spec require this **sequence**. Later steps depend on earlier ones.

| Order | Category | What your TIS does | Your goal mapping |
|-------|----------|---------------------|-------------------|
| 1 | **Initialization** | Call device init with PIN, branch office ID, equipment info. Get and store **communication key**. | Required before anything else. |
| 2 | **Basic data** | Get code list, item classification list, PIN information, branch list (head office/store), notice list from eTIMS. | Needed for correct codes in sales/items. |
| 3 | **Branch information** | Send customer (head & branch) info, branch user accounts (and insurance if pharmacy). | Required before items/sales. |
| 4 | **Item management** | Send item information (and composition if needed). Get item list. | **① Inventory** – item master. |
| 5 | **Imported item** (if applicable) | Get imported items; send converted item info. | Optional (imports). |
| 6 | **Sales management** | Send **sales transaction** then **sales invoice**. For credit notes: use the cancel/refund or credit-note service in the Technical Spec. | **② Sales + Credit notes**. |
| 7 | **Purchase transaction** | **Get** purchase transactions; send purchase confirmation. | **③ Purchases**. |
| 8 | **Stock management** | Send stock in/out; send stock inventory. Stock in/out must have corresponding sales invoice sent first where applicable. | **① Inventory** – stock levels. |

So for your three aims:

- **① Manage inventory** → Implement **Item management** (send item info, get item list) and **Stock management** (send stock in/out, send stock inventory), after initialization and branch info.
- **② Create a sale; create a credit note** → Implement **Sales management** (sales transaction + sales invoice); then the **credit note / cancel / refund** services from the Technical Spec.
- **③ Get purchases (and other KRA-supported things)** → Implement **Purchase transaction management** (get purchase transactions, send confirmation) and **Basic data** (get codes, PIN list, notices, etc.).

---

## 5. Endpoints and Environments

From the step-by-step guide:

- **Sandbox base URL:** `https://etims-api-sbx.kra.go.ke`
- **Production base URL:** `https://etims-api.kra.go.ke`

Example for device activation (Technical Spec gives the exact path, often `/selectInitOsdcInfo`):

- Sandbox: `https://etims-api-sbx.kra.go.ke/selectInitOsdcInfo`

All other service paths (item, sales, stock, purchase, etc.) are in the **TIS for OSCU/VSCU Technical Specifications v2.0** PDF: request/response format, URL path, and authentication (e.g. how to send the communication key).

---

## 6. Practical Implementation Checklist

1. **Read the Technical Spec v2.0**
   - Section 2.2 (and related): initialization, main configurations, technical policies.
   - Exact URL paths and request bodies for: init, basic data, branch, **item**, **sales**, **credit note/cancel**, **purchase**, **stock**.

2. **Get your Integration Token (if portal requires it)**
   - Complete and submit the [eTIMS Bio Data Form for OSCU and VSCU](https://www.kra.go.ke/images/publications/eTIMS-Bio-Data-Form-for-OSCU-and-VSCU.pdf) to KRA eTIMS Operations. After certification, KRA issues your Integration Token (see Section 0).

3. **Onboard one test business (sandbox)**
   - Sign up at https://etims-sbx.kra.go.ke with a test PIN.
   - Submit **Service Request → eTIMS → OSCU** (or VSCU). Enter your **Integration Token** and click **Verify**. Upload commitment form. Wait for approval SMS.
   - After approval, get branch office ID (and serial/equipment if required) from the portal or step-by-step guide.

4. **Implement initialization in your backend**
   - POST to `https://etims-api-sbx.kra.go.ke/selectInitOsdcInfo` (or path in spec) with PIN, branch office ID, equipment info.
   - Parse and store the **communication key** (and any token/cert) for that connection. Use it for all subsequent calls.

5. **Implement in sequence**
   - Basic data (get codes, branch list, etc.).
   - Branch information (send customer/branch and user accounts).
   - **Item management** → inventory item master.
   - **Sales management** → sales transaction + sales invoice; then credit note flow from spec.
   - **Purchase transaction** → get purchases, send confirmation.
   - **Stock management** → stock in/out, stock inventory.

6. **Map accounting tool ↔ eTIMS**
   - Your sync-to-books (or similar) layer: transform accounting tool entities (invoices, items, stock, purchases) to eTIMS format and back; call the right OSCU endpoints in the right order; handle ETR receipts and errors.

---

## 7. Summary

| Your goal | eTIMS category | Action |
|-----------|-----------------|--------|
| **① Manage inventory** | Item management + Stock management | Send/get items; send stock in/out and stock inventory (after init and branch). |
| **② Create sale + credit note** | Sales management | Send sales transaction then sales invoice; implement credit note (or cancel/refund) per Technical Spec. |
| **③ Get purchases and more** | Purchase transaction + Basic data | Get purchase transactions, send confirmation; get codes, PIN list, notices as needed. |

If the portal requires an **Integration Token** for both OSCU and VSCU, obtain it by applying for **certification** with the [eTIMS Bio Data Form](https://www.kra.go.ke/images/publications/eTIMS-Bio-Data-Form-for-OSCU-and-VSCU.pdf) (see Section 0). After certification, use your token on the Service Request form; then use the credentials (PIN, branch office ID, communication key) from device initialization for all API calls. Use the [Technical Spec v2.0](https://kra.go.ke/images/publications/TIS-for-OSCU--VSCU-Technical-Specifications-v2.0.pdf) for exact APIs and the [Step-by-Step Guide](https://www.kra.go.ke/images/publications/OSCU_VSCU_Step-by-Step_Guide-on-how-to-sign-up.pdf) for sign-up, approval, and sequence.
