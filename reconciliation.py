import os
print("Current Folder:", os.getcwd())


import pandas as pd

# Load datasets
transactions = pd.read_csv("transactions.csv")
settlements = pd.read_csv("settlements.csv")

# Convert dates
transactions['date'] = pd.to_datetime(transactions['date'])
settlements['settlement_date'] = pd.to_datetime(settlements['settlement_date'])

# Step 1: Detect duplicates
transactions['is_duplicate'] = transactions.duplicated(subset=['transaction_id'], keep=False)

# Step 2: Merge
merged = pd.merge(transactions, settlements, on='transaction_id', how='outer', indicator=True)

# Fill NaN for duplicate flag
merged['is_duplicate'] = merged['is_duplicate'].fillna(False)

# Step 3: Classification function
def classify(row):

    # Case 1: Missing settlement
    if row['_merge'] == 'left_only':
        if pd.notna(row['amount_x']) and row['amount_x'] < 0:
            return "Refund without original"
        return "Missing Settlement"

    # Case 2: Missing transaction
    if row['_merge'] == 'right_only':
        return "Missing Transaction"

    # Case 3: Duplicate
    if row['is_duplicate']:
        return "Duplicate Entry"

    # Case 4: Timing Issue
    if pd.notna(row['date']) and pd.notna(row['settlement_date']):
        if row['settlement_date'].month != row['date'].month:
            return "Timing Issue"

    # Case 5: Amount mismatch
    if pd.notna(row['amount_x']) and pd.notna(row['amount_y']):
        if abs(row['amount_x'] - row['amount_y']) > 0.01:
            return "Amount Mismatch"

    return "Matched"

# Step 4: Apply classification
merged['Status'] = merged.apply(classify, axis=1)

# Step 5: Clean output
final_report = merged[['transaction_id', 'amount_x', 'amount_y', 'date', 'settlement_date', 'Status']]

final_report.columns = [
    'Transaction_ID',
    'Transaction_Amount',
    'Settlement_Amount',
    'Transaction_Date',
    'Settlement_Date',
    'Status'
]

# Step 6: Save output
final_report.to_csv("report.csv", index=False)

print("\n" + "=" * 60)
print("Reconciliation Completed! Report saved as report.csv")
print("=" * 60 + "\n")

print(final_report)