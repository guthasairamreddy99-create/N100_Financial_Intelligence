import pandas as pd

path = "data/raw/sectors.xlsx"

print("Header = 0")
df0 = pd.read_excel(path, engine="openpyxl", header=0)
print(df0.head())
print(df0.columns.tolist())

print("\n" + "=" * 60 + "\n")

print("Header = 1")
df1 = pd.read_excel(path, engine="openpyxl", header=1)
print(df1.head())
print(df1.columns.tolist())