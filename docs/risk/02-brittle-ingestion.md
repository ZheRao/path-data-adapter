# Brittle Ingestion: Email-Based Delivery via Outlook + Power Automate

This document exists to make one thing unmissable:

⚠️ **Email is not infrastructure.**  
⚠️ This ingestion method is probabilistic, policy-driven, and can break without any code changes.

The purpose of this doc is to prevent accidental over-reliance on the email landing layer and to codify safeguards + failure contracts.


## 1. What This Ingestion Layer Does

PATH delivers daily data via an automated email (`system@wsapath.com`) with an attachment.

Power Automate performs:
1. Trigger on incoming email
2. Extract attachment
3. Save file into OneDrive landing folder
4. Downstream pipeline reads the saved file

This is a convenience integration, not a durable transfer protocol.


## 2. Why This Is Brittle (Root Causes)

Email ingestion is brittle because it depends on systems that were designed for human communication, not data delivery:

- Outlook / Exchange spam classification is **probabilistic**
- Messages may be routed to **Junk** per-message
- Client (Outlook Desktop) and Web (OWA) can show different states until sync
- Attachment semantics can vary (metadata vs bytes)
- Organizational security / retention policies can change behavior without notice
- Power Automate trigger behavior can vary based on message shape and attachment materialization

**Result:** the pipeline can stop receiving new data even if PATH continues sending it.


## 3. Real Failure Case Observed

### Symptom
- Automated PATH emails appeared in Inbox briefly
- When Outlook Desktop opened, emails “disappeared”
- Emails were not in Deleted Items
- Pipeline failed to ingest new daily files

### Root Cause
Emails were inconsistantly being classified into **Junk Email** (server/client classification + sync reconciliation).

### Impact
- New daily attachment file not saved into OneDrive landing folder
- Downstream job fell back to previous day (until fallback exhausted)
- Risk of silent staleness without monitoring


## 4. Mandatory Safeguards (If Email Delivery Must Remain)

### 4.1 Sender / Domain Whitelisting (Required)

To prevent PATH emails from being routed to Junk:

- Add sender/domain to Safe Senders (server-side):
  - `system@wsapath.com` and/or `@wsapath.com`
- In Outlook Desktop, mark a PATH email as **Not Junk** and select:
  - “Always trust email from this sender”
- Optionally disable client-side junk filtering in Outlook Desktop to reduce reclassification

> Without sender safeguarding, ingestion can break unpredictably.

### 4.2 Folder Coverage (Recommended)

If feasible, configure automation to ingest from both:
- Inbox (expected)
- Junk Email (defensive)

This makes junk classification non-fatal.

## 5. Pipeline Contract: Data Availability & Fallback

Downstream consumption follows a strict fallback contract:

1. Attempt to read **today’s file**
2. If unavailable, read **yesterday’s file**
3. If unavailable, **hard fail**

This is intentional:
- avoids silent corruption
- keeps operations running briefly during transient issues
- surfaces prolonged ingestion failures loudly

**Operational rule:** fallback usage must be logged and monitored.


## 6. Monitoring Requirements (Minimum)

At minimum, the system should detect missing daily files.

Recommended checks:
- If today’s file is missing by expected time → warn
- If fallback is used → warn
- If two consecutive days missing → fail + escalate


## 7. Long-Term Fix (Preferred Direction)

Email should be treated as a temporary landing mechanism. Prefer one of:

- Microsoft Graph polling / webhook ingestion (explicit control)
- SharePoint/OneDrive direct drop location from sender
- API-based delivery / blob storage / SFTP

This reduces probabilistic behavior and makes ingestion an explicit system boundary.

