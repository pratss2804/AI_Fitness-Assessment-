# AI Reconciliation System

## 📌 Problem Statement
In payment systems, transactions are recorded instantly, while bank settlements happen after a delay (1–2 days). Due to this delay, mismatches occur during reconciliation at month end.

---

## 🚀 Solution
This project implements a reconciliation system that:
- Matches transactions with settlements using transaction_id
- Detects and categorizes mismatches
- Generates a clean report with reasons

---

## 🔍 Gap Types Covered
1. Timing Issue (Settlement in next month)
2. Amount Mismatch (Rounding differences)
3. Duplicate Entry
4. Missing Settlement
5. Missing Transaction
6. Refund without original transaction

---

## ⚙️ Approach
- Generated synthetic datasets for transactions and settlements
- Performed outer join using pandas
- Applied classification logic to detect mismatches
- Generated final report (CSV)

---

## 📊 Output
The system generates a file:
reconciliation_report.csv

It contains:
- Transaction ID
- Transaction Amount
- Settlement Amount
- Dates
- Status (Matched / Mismatch Reason)

---

## 🧠 Assumptions
- Matching is based on transaction_id
- Settlement delay can be 1–2 days
- Amount difference tolerance: ±0.01
- Duplicate detection is based on transaction_id

---

## ▶️ How to Run
```bash
python reconciliation.py
