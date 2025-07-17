import pandas as pd

# Load the CSV file
df = pd.read_csv("synthetic_vitals.csv")

# Get the number of rows and calculate the midpoint
mid_index = len(df) // 2

# Split into two DataFrames
df_part1 = df.iloc[:mid_index]
df_part2 = df.iloc[mid_index:]

# Save to new CSV files
df_part1.to_csv("client1_data.csv", index=False)
df_part2.to_csv("client2_data.csv", index=False)

print("CSV file has been split into client1_data.csv and client2_data.csv.")
