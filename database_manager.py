import pandas as pd
import os
from file_utils import clean_type_name

def get_database_path(output_folder):
    """Return the absolute path to the type database CSV in the output folder."""
    return os.path.join(output_folder, "STOCK_DATABASE.csv")

def initialize_database_from_excel(output_folder, input_excel, type_column):
    """
    If database CSV does not exist, create it from the input Excel.
    All new types get status 'pending download'.
    """
    db_csv = get_database_path(output_folder)
    if os.path.exists(db_csv):
        return  # Already initialized

    df = pd.read_excel(input_excel)
    types = [str(t).strip() for t in df[type_column].dropna().unique() if str(t).strip() != ""]
    records = []
    for t in types:
        clean_t = clean_type_name(t)
        records.append({'Type': t, 'CleanType': clean_t, 'status': 'pending download'})
    db_df = pd.DataFrame(records)
    db_df.to_csv(db_csv, index=False)

def read_database(output_folder):
    """Read the database CSV as a DataFrame."""
    db_csv = get_database_path(output_folder)
    return pd.read_csv(db_csv)

def get_pending_types(output_folder):
    """Return DataFrame rows where status == 'pending download'."""
    df = read_database(output_folder)
    return df[df['status'] == 'pending download'].copy()

def mark_type_successful(output_folder, clean_type):
    """Set status to 'successfully downloaded from all 3 sources' for the given CleanType."""
    db_csv = get_database_path(output_folder)
    df = pd.read_csv(db_csv)
    df.loc[df['CleanType'] == clean_type, 'status'] = 'successfully downloaded from all 3 sources'
    df.to_csv(db_csv, index=False)