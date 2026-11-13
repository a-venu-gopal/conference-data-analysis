"""
Week 2 - Day 1: clean the raw registration data.

Fixes the problems added in generate_data.py:
  1. Extra spaces and wrong UPPER/lower case in text columns
  2. The same country written different ways ("USA" vs "United States")
  3. Missing countries
  4. Duplicate registrations
  5. Broken email addresses (flagged, not deleted - the person still registered)

Run:     python clean_data.py
Input:   data/registrations_raw.csv
Output:  data/registrations_clean.csv
"""

from pathlib import Path

import pandas as pd

RAW = Path("data/registrations_raw.csv")
CLEAN = Path("data/registrations_clean.csv")

# Short forms that should become one official name
COUNTRY_ALIASES = {
    "usa": "United States",
    "us": "United States",
    "u.s.a.": "United States",
    "uk": "United Kingdom",
}

EMAIL_PATTERN = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"


def standardise(series: pd.Series, aliases: dict | None = None) -> pd.Series:
    """
    Make every spelling of a value match its most common spelling.
    e.g. "INDIA  ", "india" and "India" all become "India".
    """
    cleaned = series.str.strip()
    key = cleaned.str.lower()
    if aliases:  # "usa" is grouped together with "united states"
        key = key.replace({k: v.lower() for k, v in aliases.items()})
    # For each lowercase key, pick the spelling that appears most often
    best = (pd.DataFrame({"key": key, "value": cleaned})
            .dropna()
            .groupby("key")["value"]
            .agg(lambda s: s.value_counts().idxmax()))
    return key.map(best)


def main() -> None:
    df = pd.read_csv(RAW)
    report = {"Rows in raw file": len(df)}

    # 1) Trim spaces in every text column
    text_cols = ["city", "first_name", "last_name", "email", "country",
                 "affiliation_type", "registration_type", "track"]
    df[text_cols] = df[text_cols].apply(lambda col: col.str.strip())

    # 2) Fix spelling / case differences
    before = df["country"].nunique()
    df["country"] = standardise(df["country"], COUNTRY_ALIASES)
    report["Country spellings fixed"] = before - df["country"].nunique()

    before = df["track"].nunique()
    df["track"] = standardise(df["track"])
    report["Track spellings fixed"] = before - df["track"].nunique()

    # 3) Missing countries -> "Unknown" (keep the row, it is still a registration)
    report["Missing countries"] = int(df["country"].isna().sum())
    df["country"] = df["country"].fillna("Unknown")

    # 4) Duplicates: same registration_id means the same person
    report["Duplicates removed"] = int(df.duplicated("registration_id").sum())
    df = df.drop_duplicates("registration_id", keep="first")

    # 5) Flag broken emails
    df["email"] = df["email"].str.lower()
    df["email_valid"] = df["email"].str.match(EMAIL_PATTERN)
    report["Invalid emails flagged"] = int((~df["email_valid"]).sum())

    # 6) Correct data types + one helpful new column
    df["registration_date"] = pd.to_datetime(df["registration_date"])
    df["attended"] = df["attended"].astype(bool)
    event_start = {2025: "2025-11-03", 2026: "2026-11-02"}
    df["days_before_event"] = (
        pd.to_datetime(df["edition"].map(event_start)) - df["registration_date"]
    ).dt.days

    df = df.sort_values("registration_id").reset_index(drop=True)
    df.to_csv(CLEAN, index=False)

    report["Rows in clean file"] = len(df)
    print("=== Cleaning report ===")
    for label, value in report.items():
        print(f"{label:<26}{value:>6,}")
    print(f"\nCountries now: {sorted(df['country'].unique())}")
    print(f"\nSaved to {CLEAN}")


if __name__ == "__main__":
    main()