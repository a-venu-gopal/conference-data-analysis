"""
Week 2 - Days 3-4: answer the business questions with SQL (SQLite).

Loads the clean CSV into a SQLite database, then runs one SQL query
per question from the README. Results are printed and saved to outputs/.

Run:     python sql_analysis.py
Input:   data/registrations_clean.csv
Output:  data/conference.db  +  outputs/q1_...csv to outputs/q5_...csv
"""

import sqlite3
from pathlib import Path

import pandas as pd

CLEAN = Path("data/registrations_clean.csv")
DB = Path("data/conference.db")
OUT = Path("outputs")

QUERIES = {
    "q1_growth_by_edition": """
        -- Q1: How did registrations grow between editions?
        SELECT
            edition,
            COUNT(*) AS registrations,
            ROUND(100.0 * (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY edition))
                  / LAG(COUNT(*)) OVER (ORDER BY edition), 1) AS growth_pct
        FROM registrations
        GROUP BY edition
        ORDER BY edition;
    """,
    "q2_track_popularity": """
        -- Q2: Which research tracks are most popular? (share % per edition)
        SELECT
            edition,
            track,
            COUNT(*) AS registrations,
            ROUND(100.0 * COUNT(*)
                  / SUM(COUNT(*)) OVER (PARTITION BY edition), 1) AS share_pct
        FROM registrations
        GROUP BY edition, track
        ORDER BY edition, registrations DESC;
    """,
    "q3_country_share": """
        -- Q3: Which countries send the most participants? (% share)
        SELECT
            country,
            COUNT(*) AS registrations,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM registrations), 1)
                AS share_pct
        FROM registrations
        GROUP BY country
        ORDER BY registrations DESC;
    """,
    "q4_registration_timing": """
        -- Q4: How early do people register before the event?
        SELECT
            CASE
                WHEN days_before_event <= 30  THEN '1) Last month'
                WHEN days_before_event <= 90  THEN '2) 1-3 months before'
                WHEN days_before_event <= 180 THEN '3) 3-6 months before'
                ELSE                               '4) 6+ months before'
            END AS window,
            COUNT(*) AS registrations,
            ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM registrations), 1)
                AS share_pct
        FROM registrations
        GROUP BY window
        ORDER BY window;
    """,
    "q5_attendance_rate": """
        -- Q5: What share of registrants actually attend?
        SELECT
            edition,
            registration_type,
            COUNT(*) AS registrations,
            ROUND(100.0 * SUM(attended) / COUNT(*), 1) AS attendance_pct
        FROM registrations
        GROUP BY edition, registration_type
        ORDER BY edition, attendance_pct DESC;
    """,
}


def main() -> None:
    df = pd.read_csv(CLEAN)
    df["attended"] = df["attended"].astype(int)  # SQLite stores True/False as 1/0

    OUT.mkdir(exist_ok=True)
    with sqlite3.connect(DB) as conn:
        # Write the table (replace it if it already exists from an earlier run)
        df.to_sql("registrations", conn, if_exists="replace", index=False)
        print(f"Loaded {len(df):,} rows into {DB} (table: registrations)\n")

        for name, sql in QUERIES.items():
            result = pd.read_sql_query(sql, conn)
            result.to_csv(OUT / f"{name}.csv", index=False)
            title = sql.strip().splitlines()[0].lstrip("- ")
            print(f"=== {title} ===")
            print(result.to_string(index=False), "\n")

    print(f"Results saved in {OUT}/")


if __name__ == "__main__":
    main()