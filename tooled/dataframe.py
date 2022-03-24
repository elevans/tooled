import pandas as pd
from typing import List

def extract_column_as_dataframe(column: str, dataframe: pd.DataFrame) -> List[pd.DataFrame]:
    """Extract a column's unique values as a List of DataFrames.

    The unique values of a column are used to extract DataFrames in a List.
    For example this would be useful for splitting a large DataFrame into smaller ones
    based on unique 'condition' or 'sample' columns.

    :param column: The column to extract.
    :param dataframe: Input DataFrame.
    :return: List of DataFrames.
    """
    unique_column_vals = set(dataframe[column].to_list())
    dfs = []
    for val in unique_column_vals:
        dfs.append(dataframe[dataframe[column] == val])

    return dfs