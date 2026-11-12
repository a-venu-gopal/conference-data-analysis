"""
Week 1: first look at the data with pandas.

Run:  python explore.py
"""

import pandas as pd

df = pd.read_csv("data/registrations_raw.csv")

print("=== Shape (rows, columns) ===")
print(df.shape)

print("\n=== First 5 rows ===")
print(df.head())

print("\n=== Column types ===")
print(df.dtypes)

print("\n=== Missing values per column ===")
print(df.isna().sum())

print("\n=== Duplicate rows ===")
print(df.duplicated().sum())

print("\n=== Registrations per edition ===")
print(df["edition"].value_counts().sort_index())

print("\n=== Top 10 countries (share %) ===")
print((df["country"].value_counts(normalize=True).head(10) * 100).round(1))

print("\n=== Registration type share % ===")
print((df["registration_type"].value_counts(normalize=True) * 100).round(1))

print("\n=== Spelling problems to fix in Week 2 (unique country values) ===")
print(sorted(df["country"].dropna().unique()))
