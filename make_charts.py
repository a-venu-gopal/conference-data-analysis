"""
Week 2 - Days 5-6: turn the SQL results into charts.

Run:     python make_charts.py   (run sql_analysis.py first)
Input:   data/registrations_clean.csv + outputs/q*.csv
Output:  images/*.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUT = Path("outputs")
IMG = Path("images")
COLORS = {2025: "#9db4d6", 2026: "#1f4e9c"}  # light blue = 2025, dark blue = 2026

sns.set_theme(style="whitegrid", font_scale=1.0)


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(IMG / name, dpi=150)
    plt.close(fig)
    print(f"Saved {IMG / name}")


def chart_registration_trend() -> None:
    """Q1: cumulative registrations in the weeks before each event."""
    df = pd.read_csv("data/registrations_clean.csv")
    df["weeks_before"] = df["days_before_event"] // 7
    growth = pd.read_csv(OUT / "q1_growth_by_edition.csv")["growth_pct"].iloc[-1]

    fig, ax = plt.subplots(figsize=(9, 5))
    for edition, group in df.groupby("edition"):
        weekly = group["weeks_before"].value_counts().sort_index(ascending=False)
        ax.plot(weekly.index, weekly.cumsum(), label=str(edition),
                color=COLORS[edition], linewidth=2.5)
    ax.invert_xaxis()  # countdown: far from the event on the left, event day on the right
    ax.set(title=f"Registrations build-up before the event (2026: +{growth:.1f}% vs 2025)",
           xlabel="Weeks before the event", ylabel="Total registrations so far")
    ax.legend(title="Edition")
    save(fig, "1_registration_trend.png")


def chart_track_popularity() -> None:
    """Q2: share of registrations per track, both editions side by side."""
    df = pd.read_csv(OUT / "q2_track_popularity.csv")
    order = (df[df["edition"] == 2026].sort_values("share_pct", ascending=False)["track"])

    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.barplot(data=df, y="track", x="share_pct", hue="edition", order=order,
                palette=COLORS, ax=ax)
    ax.set(title="Track popularity (% of each edition's registrations)",
           xlabel="Share of registrations (%)", ylabel="")
    ax.legend(title="Edition", bbox_to_anchor=(1.01, 1), loc="upper left")
    save(fig, "2_track_popularity.png")


def chart_country_share() -> None:
    """Q3: country share %, top 10 + all others grouped."""
    df = pd.read_csv(OUT / "q3_country_share.csv")
    top = df.head(10).copy()
    other = pd.DataFrame([{"country": "All others",
                           "share_pct": round(df["share_pct"].iloc[10:].sum(), 1)}])
    df = pd.concat([top, other], ignore_index=True)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(df["country"], df["share_pct"], color="#1f4e9c")
    bars[-1].set_color("#bbbbbb")  # grey for the "All others" group
    ax.bar_label(bars, fmt="%.1f%%", padding=3)
    ax.set_xlim(0, df["share_pct"].max() * 1.12)  # room for the % labels
    ax.invert_yaxis()  # biggest at the top
    ax.set(title="Participants by country (% share, both editions)",
           xlabel="Share of registrations (%)", ylabel="")
    save(fig, "3_country_share.png")


def chart_registration_timing() -> None:
    """Q4: how early people register."""
    df = pd.read_csv(OUT / "q4_registration_timing.csv")
    df["window"] = df["window"].str[3:]  # drop the "1) " sort prefix for display

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(df["window"], df["share_pct"], color="#1f4e9c")
    ax.bar_label(bars, fmt="%.1f%%", padding=3)
    ax.set(title="When do people register?", xlabel="", ylabel="Share of registrations (%)")
    ax.set_ylim(0, df["share_pct"].max() * 1.15)
    save(fig, "4_registration_timing.png")


def chart_attendance() -> None:
    """Q5: attendance rate by registration type and edition."""
    df = pd.read_csv(OUT / "q5_attendance_rate.csv")

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=df, x="registration_type", y="attendance_pct", hue="edition",
                palette=COLORS, ax=ax)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f%%", padding=2, fontsize=9)
    ax.set(title="Attendance rate by registration type", xlabel="",
           ylabel="Registrants who attended (%)", ylim=(0, 105))
    ax.legend(title="Edition", bbox_to_anchor=(1.01, 1), loc="upper left")
    save(fig, "5_attendance_rate.png")


def main() -> None:
    IMG.mkdir(exist_ok=True)
    chart_registration_trend()
    chart_track_popularity()
    chart_country_share()
    chart_registration_timing()
    chart_attendance()


if __name__ == "__main__":
    main()