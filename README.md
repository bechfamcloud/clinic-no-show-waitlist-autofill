# Clinic No-Show & Waitlist Auto-Fill (Serverless)

A serverless, event-driven AWS solution that detects **appointment no-shows** and automatically **promotes the next eligible patient from a waitlist** into the freed slot — built with a DynamoDB single-table design, Lambda, and EventBridge, using least-privilege IAM.

---

## Business Problem

Healthcare clinics lose revenue and operational efficiency when patients:
- Miss scheduled appointments (**no-shows**)
- Leave open slots unfilled due to manual waitlist handling
- Require staff time to “call down the waitlist” and rebook

This project automates that workflow safely and auditablely.

---

## What This Project Demonstrates

- **DynamoDB single-table design** for scheduling + waitlist + reservations
- **GSI-based access patterns** for efficient querying (GSI1)
- **TTL-based holds** for reservation locks (auto-expiry)
- **Lambda processing** for:
  - Detecting no-show conditions
  - Releasing slots
  - Promoting waitlist patients
  - Updating appointment + waitlist states
- **EventBridge scheduled rule** invoking Lambda on a fixed rate using **Constant JSON input**
- **Least-privilege IAM** (custom policy scoped to required DynamoDB actions/resources)
- **CloudWatch logs** as execution proof

---

## High-Level Architecture

**EventBridge (Schedule) → Lambda (clinic-no-show-processor) → DynamoDB (ClinicScheduling)**  
Supporting services: **IAM (least privilege)**, **CloudWatch Logs**.

---

## Data Model (DynamoDB: `ClinicScheduling`)

### Primary Key
- **PK** (String)
- **SK** (String)

### Global Secondary Index
- **GSI1PK** (String)
- **GSI1SK** (String)

### Entities in the same table
- **APPT**: Appointment metadata and state
- **WAIT**: Waitlist request(s)
- **RESV / HOLD**: Slot reservation lock to prevent double booking

---

## Access Patterns Verified

### 1) Query appointments by clinic + day (GSI1)
- **GSI1PK**: `CLINIC#<clinicId>#DAY#<YYYY-MM-DD>`
- **GSI1SK**: `T#<ISO>#APPT#<appointmentId>`

✅ Verified in DynamoDB console: GSI1 query returned expected appointment (`A1001`).

### 2) Query waitlist by clinic + service + day
Waitlist items were queried successfully (e.g., returned `P9002` / subsequent waitlist entries).

---

## TTL (Time To Live) Hold / Reservation

Reservation locks use a TTL attribute so holds expire automatically (safety + cleanup).
- TTL enabled on the table
- Lock items store an epoch timestamp TTL
- Verified lock behavior:
  - **First run**: lock acquired (`slotLockAcquired = true`)
  - **Second run** (within hold window): lock not acquired (`slotLockAcquired = false`)

---

## Lambda Function

### Function
- Name: `clinic-no-show-processor`
- Runtime: Python 3.11
- Memory: 128 MB

### Environment Variables (configured)
- `TABLE_NAME`
- `DEFAULT_CLINIC_ID`

### What the function does (core flow)
1. Reads inputs (from test event or EventBridge)
2. Queries DynamoDB (via GSI1 and/or patterns used in code)
3. Applies conditional updates to avoid race conditions
4. Uses/creates a reservation lock (HOLD/RESV) with TTL
5. Updates:
   - appointment status (e.g., `NO_SHOW`, `SCHEDULED`)
   - waitlist status (e.g., `WAITING`, `OFFERED`, etc.)
6. Returns a JSON response with outcome flags

---

## Execution Proof

### A) Manual Lambda Test (Console)
Test event executed successfully and returned the expected response body.

**Key boolean outcomes returned (the “3 booleans”):**
- `slotLockAcquired`  
- `appointmentStatusUpdated`  
- `waitlistStatusUpdated`

✅ Confirmed scenarios:
- Hold acquisition `true` (first run), `false` (repeat run while locked)
- No-show processing updated statuses successfully
- All three booleans observed as `true` after successful update sequence

### B) EventBridge → Lambda (Scheduled Trigger)
A scheduled rule invoked the Lambda using **Constant JSON input**.

✅ CloudWatch Logs show:
- `INIT_START` / `START` / `END` / `REPORT` lifecycle
- Automatic invocation on schedule
- “No scheduled appointments found (nothing to process)” when appropriate

---

## EventBridge Configuration

### Rule
- Type: Scheduled rule
- Input: **Constant (JSON)** (not “Matched event”)

Example Constant JSON used:
```json
{
  "clinicId": "001",
  "date": "2026-02-10"
}
