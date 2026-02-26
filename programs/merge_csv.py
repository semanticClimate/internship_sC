import pandas as pd
import os
import glob

# Folder containing CSV files
folder_path = "csv_files"   # change this to your folder name

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# Read and combine all CSV files
dataframes = []
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

merged_df = pd.concat(dataframes, ignore_index=True)

# Save merged CSV
merged_df.to_csv("merged_keywords.csv", index=False)

print("All CSV files merged successfully!")
