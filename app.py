import streamlit as st
import pandas as pd

st.title("AI Reconciliation System")

# Upload files
transactions_file = st.file_uploader("Upload Transactions CSV", type=["csv"])
settlements_file = st.file_uploader("Upload Settlements CSV", type=["csv"])

if transactions_file and settlements_file:

    transactions = pd.read_csv(transactions_file)
    settlements = pd.read_csv(settlements_file)

    # Convert dates
    transactions['date'] = pd.to_datetime(transactions['date'])
    settlements['settlement_date'] = pd.to_datetime(settlements['settlement_date'])

    # Detect duplicates
    transactions['is_duplicate'] = transactions.duplicated(subset=['transaction_id'], keep=False)

    # Merge
    merged = pd.merge(transactions, settlements, on='transaction_id', how='outer', indicator=True)
    merged['is_duplicate'] = merged['is_duplicate'].fillna(False)

    # Classification
    def classify(row):
        if row['_merge'] == 'left_only':
            if pd.notna(row['amount_x']) and row['amount_x'] < 0:
                return "Refund without original"
            return "Missing Settlement"

        if row['_merge'] == 'right_only':
            return "Missing Transaction"

        if row['is_duplicate']:
            return "Duplicate Entry"

        if pd.notna(row['date']) and pd.notna(row['settlement_date']):
            if row['settlement_date'].month != row['date'].month:
                return "Timing Issue"

        if pd.notna(row['amount_x']) and pd.notna(row['amount_y']):
            if abs(row['amount_x'] - row['amount_y']) > 0.01:
                return "Amount Mismatch"

        return "Matched"

    merged['Status'] = merged.apply(classify, axis=1)

    final_report = merged[['transaction_id', 'amount_x', 'amount_y', 'date', 'settlement_date', 'Status']]
    final_report.columns = [
        'Transaction_ID', 'Transaction_Amount', 'Settlement_Amount',
        'Transaction_Date', 'Settlement_Date', 'Status'
    ]

    st.success("Reconciliation Completed!")

    st.dataframe(final_report)

    # Download button
    csv = final_report.to_csv(index=False).encode('utf-8')
    st.download_button("Download Report", csv, "reconciliation_report.csv", "text/csv")