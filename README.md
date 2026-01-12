# Clinic No-Show & Waitlist Auto-Fill (Serverless)

## Overview
Healthcare clinics lose revenue and efficiency due to patient no-shows.  
This project demonstrates a **serverless, event-driven AWS architecture** that detects appointment no-shows and automatically fills open slots from a waitlist.

The solution is designed with **least-privilege IAM**, scalability, and operational simplicity in mind.

---

## Business Problem
- Patients miss scheduled appointments (no-shows)
- Clinics lose time and revenue
- Manual waitlist handling is inefficient

---

## Solution Architecture (High Level)
- Amazon S3 for event logging and artifacts
- AWS Lambda for no-show detection and processing
- IAM roles with least-privilege permissions
- Event-driven workflow (future labs)

---

## Project Structure
```text
.
├── docs/          # Architecture, design decisions, lab notes
├── infra/         # IAM policies and infrastructure artifacts
├── src/           # Lambda function source code
├── screenshots/   # Console and architecture screenshots
└── README.md

