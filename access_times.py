import os

import matplotlib.pyplot as plt
# Sample data
import pandas as pd


def read_csv_filter_convert(file_path_local, column_names, numeric_tail, delimiter='|'):
    """
    Reads a CSV file, filtering lines with exactly len(column_names) columns and where the last {numeric_tail} columns must be numeric.

    Parameters:
    - file_path: Path to the CSV file.

    Returns:
    - A DataFrame containing valid rows.
    - The count of fields that could not be converted to numbers.
    """
    valid_rows = []  # List to store valid rows
    non_convertible_count = 0  # Count of non-convertible fields

    with open(file_path_local, 'r') as file:
        for line in file:
            columns = line.strip().split(delimiter)  # Assuming '|' as the delimiter, adjust if necessary

            if len(columns) == len(column_names):  # Check if the line has exactly 3 columns
                try:
                    # Attempt to convert 2nd and 3rd columns to floats
                    for item in range(1, numeric_tail + 1):
                        columns[-item] = float(columns[-item])
                    valid_rows.append(columns)  # Add to valid rows if successful
                except ValueError:
                    # Count each failed conversion attempt
                    non_convertible_count += 1

    # Create DataFrame from valid rows
    df = pd.DataFrame(valid_rows, columns=column_names)

    return df, non_convertible_count
