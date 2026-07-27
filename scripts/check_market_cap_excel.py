import pandas as pd

path = "data/raw/market_cap.xlsx"

print("=" * 60)
print("HEADER = 0")
print("=" * 60)

df0 = pd.read_excel(path, engine="openpyxl", header=0)
print(df0.head())
print(df0.columns.tolist())

print("\n" + "=" * 60)
print("HEADER = 1")
print("=" * 60)

df1 = pd.read_excel(path, engine="openpyxl", header=1)
print(df1.head())
print(df1.columns.tolist())