import pandas as pd

def read_file(uploaded_file):
    if uploaded_file.name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")

def validate_input(df):
    required_columns = ["Names"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Input file must contain the following columns: {', '.join(required_columns)}")
    return df
