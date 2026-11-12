# Conference Registration Data Analysis

Analysing registration data for a fictional AI conference series to find
trends in registrations, popular research tracks and country participation.

> All data in this project is **synthetic** (generated with Faker).
> No real people or contact details are included.

## What this project shows
- Generating a realistic practice dataset with Python
- Exploring and cleaning messy data with **pandas**
- Answering business questions with **SQL** (SQLite)
- Visualising results with **matplotlib** and **seaborn**

## Questions answered
1. How did registrations grow between editions?
2. Which research tracks are most popular?
3. Which countries send the most participants (as % share)?
4. How early do people register before the event?
5. What share of registrants actually attend?

## How to run
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
python generate_data.py
python explore.py
```

## Project status
- [x] Week 1: dataset generated and explored
- [ ] Week 2: cleaning, SQL analysis and charts

## Tech stack
Python · pandas · SQLite · matplotlib · seaborn
