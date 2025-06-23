import pandas as pd
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

# Example usage with the previously loaded dataframe
if 'df' in globals():
  json_df = dataframe_to_json(df)
  print(json_df)
else:
  print("DataFrame 'df' is not available. Please ensure the dataset is loaded.")
