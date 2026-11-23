# Salesforce FP&A Model

A driver-based budget and five-year forecast for Salesforce (NYSE: CRM), built from SEC filings. It includes live Bear/Base/Bull scenarios, budget-vs-actual variance analysis, and a reforecast log that is updated each quarter.

**Built by Louis Ngo** · Live dashboard: *link coming soon*

> Growth has slowed to high single digits. Margins and cash flow now carry the story.

## Key findings

- **FY26 revenue beat plan by $825M.** $41.5B against a $40.7B guidance midpoint (+2.0%), partly from the Informatica acquisition.
- **FY26 GAAP operating margin missed plan by 1.5 points.** 20.1% against a 21.6% guide, as restructuring and deal costs absorbed the revenue upside.
- **FY27 is being reforecast up on revenue, down on margin.** Across three guidance updates the revenue midpoint rose $250M, mostly from acquisitions, while GAAP margin guidance fell from 20.9% to 20.1%.
- **H2 FY27 needs a margin step-down.** H1 GAAP operating margin was 20.8%, so hitting the 20.1% full-year guide implies about 19.4% in H2.

## What's in the model

| Tab | What it shows |
|---|---|
| Overview | Headline metrics (revenue, GAAP margin, FCF, RPO, Rule of 40) and FY21–FY31 trend charts |
| Actuals | Annual P&L and cash flow for FY21–FY26, quarterly P&L, RPO history |
| Forecast | FY27E–FY31E P&L and cash flow driven by 12 inputs, with Bear/Base/Bull presets, scenario chart and operating-expense budget by function |
| Budget vs actual | FY26 guidance vs. actual variance, FY27 guidance by update, H1 pacing, reforecast log |
| Sources | Every source, the method, and known gaps |

## Method

- **Budget = company guidance.** Public companies don't publish internal budgets, so annual guidance is treated as the plan of record and each guidance update as a reforecast.
- **FY27E** is anchored to the latest guidance range. FY27E cost ratios use first-half FY27 actuals.
- **FY28E–FY31E** run off drivers: revenue growth and its annual fade, US GDP sensitivity, gross margin, each operating-expense line as a % of revenue (moving in a straight line toward FY31 targets), restructuring, operating cash flow and capex.
- **Free cash flow** = operating cash flow − capital expenditures. **Rule of 40** = revenue growth % + FCF margin %.

## Data sources

- **Financial statements and RPO:** SEC EDGAR XBRL company facts for salesforce, Inc. (CIK 0001108524), through the Q2 FY27 10-Q filed Aug 27, 2026. Pulled with `scripts/extract_sec.py`.
- **Guidance:** Salesforce quarterly results releases (Feb 26, 2025; Feb 25, 2026; May 2026; Aug 26, 2026).
- **Economic backdrop:** BEA (US GDP), IMF World Economic Outlook, Gartner IT spending forecast, Federal Reserve, BLS CPI. Links are on the dashboard's Sources tab.

## Repository layout

```
index.html                  the dashboard (self-contained HTML, no build step)
data/crm_financials.json    SEC-reported financials in $M, RPO in $B
scripts/extract_sec.py      refreshes the data from SEC EDGAR
docs/SPEC-v2.md             spec for the next version
```

## Refreshing the data

```bash
SEC_USER_AGENT="Your Name your@email.com" python scripts/extract_sec.py
```

The SEC asks automated clients to identify themselves in the User-Agent header. Fiscal years end January 31, so FY26 is Feb 2025 – Jan 2026. Q4 is derived as the full year minus Q1–Q3.

## Roadmap

- **v2 (in progress):** revenue by product cloud with organic and acquired growth separated, non-GAAP margin view, a Base case with documented rationale for each driver, and a one-page analyst memo. See `docs/SPEC-v2.md`.
- **Q3 FY27 refresh:** after Salesforce reports on Dec 2, 2026.
- **v3:** peer benchmarking (ServiceNow, Adobe, Workday, HubSpot) and an Excel version of the model.

---

Built from public filings for educational and portfolio purposes. Not investment advice.
