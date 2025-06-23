import pandas as pd
import numpy as np
from typing import Optional


def load_po_tracking_data(filepath: str) -> Optional[pd.DataFrame]:
    """
    Loads the PO tracking data from a CSV file.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A pandas DataFrame if the file is found and loaded successfully, otherwise None.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"An error occurred while loading the dataset: {e}")
        return None
    

def dataframe_to_json(df: pd.DataFrame) -> str:
    """
    Converts a pandas DataFrame to a JSON formatted string.

    Args:
        df: The input pandas DataFrame.

    Returns:
        A JSON formatted string representation of the DataFrame.
    """
    return df.to_json(orient='records', indent=2) if df is not None else "[]"


def get_po_tracking_data(filepath: str):
    """
    Loads the PO tracking data from a CSV file and returns a list of dicts with cleaned values.
    """
    df = load_po_tracking_data(filepath)
    if df is not None:
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.where(pd.notnull(df), None)
        records = df.to_dict(orient="records")
        return [clean_nans(r) for r in records]
    return None

def clean_nans(obj):
    if isinstance(obj, dict):
        return {k: clean_nans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nans(v) for v in obj]
    elif isinstance(obj, float):
        if pd.isna(obj) or obj in [np.inf, -np.inf]:
            return None
        return obj
    else:
        return obj

def get_all_po_records(filepath: str):
    df = load_po_tracking_data(filepath)
    if df is not None:
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.where(pd.notnull(df), None)
        records = df.to_dict(orient="records")
        return [clean_nans(r) for r in records]
    return None

def get_po_record_by_number(po_id: str, filepath: str):
    df = load_po_tracking_data(filepath)
    if df is not None:
        po_row = df[df['po_number'] == po_id]
        if not po_row.empty:
            po_row = po_row.replace([np.inf, -np.inf], np.nan)
            po_row = po_row.where(pd.notnull(po_row), None)
            record = po_row.to_dict(orient="records")[0]
            return clean_nans(record)
    return None
