import pandas as pd

def extract_types_from_excel(excel_path, type_column):
    """
    Extracts all unique, non-empty 'type' values from the specified column in the Excel file.
    """
    df = pd.read_excel(excel_path)
    types = df[type_column].dropna().unique()
    return [str(t).strip() for t in types if str(t).strip() != ""]