# SMT Shift Quality Dashboard

A Python full-stack project that analyses SMT inspection (SPI/AOI) data
and produces shift-wise quality dashboards and automatic reports.

## What it will do
- Calculate first-pass yield (FPY), defect rate and DPMO by line and shift
- Show a defect Pareto chart and defects-by-line chart
- Flag lines that fall below the yield target
- Generate a PDF/Excel report at the end of each shift

## Tech stack
Python, pandas, Flask, SQLite, React, reportlab/openpyxl, pytest

## Data (simulated only)
No real company data is used. Each row is one inspected board:

| Column | Example |
|---|---|
| date, shift | 2026-10-15, A |
| line | Line1 |
| board_id | B000123 |
| result | PASS / FAIL |
| defect_type | Bridging, Tombstone, Insufficient solder, Missing component, Misalignment, None |
| paste_volume_pct | 96.5 |
| reflow_peak_temp | 245 |

## Status
Day 1: project setup. Work in progress.