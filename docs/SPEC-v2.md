# Spec: Salesforce FP&A Model v2

Status: ready-for-agent · Agreed in grilling session, Nov 23, 2026 · Live v1: https://claude.ai/artifact/KHbCpp5fbkp9nkmNr5NCkC

## Problem Statement

I'm applying for FP&A analyst roles at SaaS and tech companies, and I need a portfolio piece that proves I can do the job: build a driver-based budget and forecast from real company data, explain variances against plan, and defend my assumptions. v1 works as a model, but it has three gaps. All the assumptions are the assistant's, not mine. Revenue is forecast as a single top-line growth rate, which isn't how SaaS FP&A teams work. And nothing tells a recruiter in 60 seconds what I concluded or who I am.

## Solution

Upgrade the existing dashboard, keeping the same link and the same look, into a per-cloud revenue model for Salesforce:

- Organic growth is split from acquired growth.
- The model reports both GAAP and non-GAAP margins.
- The Base case is chosen by me in a structured workshop, with my reason shown next to every assumption.
- Bear and Bull cases are defined as adjustments around my Base.
- A one-page analyst memo in my own voice leads the Overview.
- The model is published as a public GitHub repo and refreshed each quarter when Salesforce reports. The first refresh is Q3 FY27 on Dec 2, 2026.

## User Stories

### Recruiter / hiring manager (the 60-second skim)
1. As a recruiter, I want a three-sentence thesis at the top of the Overview, so that I understand the analyst's conclusion without reading the model.
2. As a recruiter, I want the author's name and LinkedIn/GitHub links in the header, so that I know whose work this is and can follow up.
3. As a recruiter, I want a short line stating which skills the project demonstrates, so that I can map it to the job description.
4. As a hiring manager, I want SaaS metrics (current RPO, attrition, Agentforce/Data Cloud ARR, subscription share) on the Overview, so that I can see the candidate speaks the language of SaaS finance.
5. As a hiring manager, I want the page to work on my phone, so that I can review it between meetings.
6. As a hiring manager, I want a "last refreshed" date and the latest reported quarter visible, so that I can tell the model is maintained.

### Interviewer (depth)
7. As an interviewer, I want revenue forecast separately for each product cloud, so that I can probe the candidate's view of each business line.
8. As an interviewer, I want organic and acquired revenue shown on separate lines, so that I can see how much growth is bought.
9. As an interviewer, I want each Base case assumption shown with the candidate's one-line reason, so that I can challenge the reasoning and not only the number.
10. As an interviewer, I want each assumption shown next to its history and company guidance, so that I can judge whether it is aggressive or conservative.
11. As an interviewer, I want a current-RPO cross-check beside the revenue forecast, so that I can see whether next-year revenue is consistent with contracted backlog.
12. As an interviewer, I want GAAP and non-GAAP operating margin shown together, so that I can discuss stock-based compensation and amortization.
13. As an interviewer, I want Bear and Bull defined as explicit changes from Base, so that I can see which drivers the candidate thinks matter most.
14. As an interviewer, I want the full memo in its own tab, so that I can read the argument end to end.
15. As an interviewer, I want the budget-vs-actual and reforecast log to keep updating each quarter, so that I can ask how the candidate's view changed.

### Analyst (me, the owner)
16. As the analyst, I want to set every Base case driver myself in a guided workshop, so that I can defend each number in an interview.
17. As the analyst, I want to see the forecast react live while I choose assumptions, so that I understand the sensitivity of each driver.
18. As the analyst, I want draft assumptions clearly marked "draft" until I lock them, so that nobody mistakes them for my view.
19. As the analyst, I want to try my own inputs with sliders and return to my Base with one click, so that I can explore without losing my case.
20. As the analyst, I want a memo drafted from my decisions that I then rewrite, so that I don't start from a blank page but still end up with my own voice.
21. As the analyst, I want the memo to double as the GitHub README, so that I maintain it in one place.
22. As the analyst, I want a repeatable refresh after each earnings release, so that keeping the model current takes minutes, not hours.
23. As the analyst, I want press-release figures marked provisional until the 10-Q is filed, so that the model is honest about its data.
24. As the analyst, I want every number traceable to a source (SEC filing, earnings release, or my assumption), so that I can answer "where did this come from?"

### Viewer (any)
25. As a viewer, I want blue to mean "hard-coded input" consistently, so that I can tell assumptions from calculations.
26. As a viewer, I want tooltips on every chart, so that I can read exact values.
27. As a viewer, I want the page to follow my light or dark theme, so that it's readable in either.

## Implementation Decisions

- **Same artifact and visual design.** v2 republishes to the v1 link. Layout, tokens, typography and the "blue = input" convention are unchanged; only content is added.
- **One forecast engine.** A single pure function takes (historical actuals, guidance anchors, inputs) and returns forecast rows per year. Every chart, table and KPI tile renders from its output. No calculation lives in rendering code.
- **Revenue build.** Total revenue = sum of five organic cloud lines + one acquired-revenue line. Each cloud has an organic growth input per year, or a starting rate plus a fade. Acquired revenue is anchored to disclosed contributions (Informatica about 3 pts of FY27 growth), with Contentful and Fin added from their close date.
- **FY27E anchor.** FY27E total revenue stays tied to the latest company guidance range. Cloud-level FY27E figures are allocated using H1 FY27 actual mix and growth.
- **Current-RPO cross-check.** Shown beside the revenue forecast as a ratio (next-year revenue ÷ current RPO), compared with history. It is a check, not a driver.
- **Non-GAAP bridge.** Non-GAAP operating income = GAAP operating income + stock-based compensation + amortization of acquired intangibles + restructuring. Each add-back is forecast as a % of revenue. Budget vs actual compares non-GAAP where the company guided non-GAAP.
- **Scenarios.** Base = the locked workshop inputs. Bear and Bull = per-driver deltas applied to Base and shown in a table. A custom state exists for slider exploration, with "Reset to my Base".
- **Assumption metadata.** Each input carries: value, low/high range, history reference, guidance reference, owner reason text, and a status (draft or locked). Reasons render next to the slider.
- **Data sources.** Cloud-level revenue comes from 10-K/10-Q revenue-disaggregation tables. Current RPO, attrition and Agentforce/Data Cloud ARR come from earnings releases. Each figure keeps a source tag and an "as reported" or "provisional" flag.
- **Memo.** Lives as one text source rendered in three places: a thesis block on the Overview (first three sentences), a Memo tab (full text), and the README.
- **Header.** "Prepared by" with name, LinkedIn and GitHub. The values come from the owner and are never invented; the header is hidden until they are provided.
- **Repo.** Public `salesforce-fpa-model`: the page, a data-extraction script (SEC EDGAR XBRL → JSON), the data snapshot, README = memo plus method notes. Blocked until GitHub is connected.
- **Refresh workflow.** After each earnings release: update quarterly actuals and pacing, append a row to the reforecast log, re-anchor FY27E to the new guide, mark the quarter provisional, then true up to the 10-Q. First run is scheduled for Dec 3, 2026.

## Testing Decisions

- **One seam: the forecast engine.** Tests call it with fixed inputs and assert on its outputs only, never on rendering or internal steps.
- **What to assert:**
  - Cloud lines plus acquired revenue sum to total revenue.
  - FY27E total sits inside the guidance range for the low, mid and high settings.
  - Historical years pass through unchanged.
  - Bear ≤ Base ≤ Bull on revenue and operating income when the deltas point that way.
  - The non-GAAP minus GAAP gap equals the sum of the add-backs.
  - Margins and Rule of 40 recompute correctly from rows.
  - Locked Base inputs reproduce the published Base numbers exactly, as a snapshot.
- **Data checks:** the extraction script's output matches published 10-K totals (for example FY26 revenue $41,525M, GAAP operating income $8,331M), and quarterly figures sum to annual figures.
- **Rendering:** one headless-browser pass per release for script errors, horizontal overflow at 400px, and light/dark theme.
- **Prior art:** none yet (no codebase). v1 was checked only by headless render; these tests start the suite.

## Out of Scope

- Peer benchmarking (ServiceNow, Adobe, Workday, HubSpot): v3.
- Downloadable Excel model: v3.
- A SaaS revenue bridge built on new-customer bookings and churn, because Salesforce doesn't disclose the inputs.
- Valuation (DCF, multiples), balance sheet forecasting, and EPS/share-count modeling.
- Live economic data feeds (FRED/BLS are unreachable from the build environment); economic inputs stay as cited published figures.
- Redesign of the visual identity.

## Further Notes

- **Owner:** Louis Ngo (header byline added). **Open item:** LinkedIn and GitHub URLs for the header.
- **Unverified input:** the IMF 2.3% US GDP outlook still comes from a secondary source and should be checked against IMF tables.
- **Known modeling caveat:** v1's FY27E GAAP margin on H1 run-rate (20.8%) sits above the company's 20.1% guide. v2 should either explain the gap in the memo or calibrate H2.
- **Key dates:** Q3 FY27 results Dec 2, 2026 (after market close); refresh reminder Dec 3, 10:00 AM ET.
