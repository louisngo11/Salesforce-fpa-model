"""Pull Salesforce (CIK 0001108524) financials from SEC EDGAR XBRL company facts.

Writes data/crm_financials.json with annual (FY) and quarterly values in $M.

Usage:
    SEC_USER_AGENT="Your Name your@email.com" python scripts/extract_sec.py
    python scripts/extract_sec.py --input companyfacts.json   # use a saved download

The SEC asks automated clients to identify themselves in the User-Agent header:
https://www.sec.gov/os/accessing-edgar-data
"""
import argparse
import json
import os
import urllib.request
from datetime import date
from pathlib import Path

CIK = "0001108524"
URL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json"

# Output key -> US-GAAP XBRL tag
TAGS = {
    "revenue": "RevenueFromContractWithCustomerExcludingAssessedTax",
    "gross_profit": "GrossProfit",
    "sales_marketing": "SellingAndMarketingExpense",
    "research_development": "ResearchAndDevelopmentExpense",
    "general_admin": "GeneralAndAdministrativeExpense",
    "restructuring": "RestructuringCharges",
    "operating_income": "OperatingIncomeLoss",
    "net_income": "NetIncomeLoss",
    "operating_cash_flow": "NetCashProvidedByUsedInOperatingActivities",
    "capex": "PaymentsToAcquirePropertyPlantAndEquipment",
    "stock_comp": "ShareBasedCompensation",
}
FLOW_ONLY_ANNUAL = {"operating_cash_flow", "capex", "stock_comp"}  # 10-Qs report these year-to-date


def load(path):
    if path:
        return json.loads(Path(path).read_text())
    ua = os.environ.get("SEC_USER_AGENT")
    if not ua:
        raise SystemExit("Set SEC_USER_AGENT (e.g. 'Your Name your@email.com') or pass --input.")
    req = urllib.request.Request(URL, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def fiscal_label(end, quarter=False):
    """Salesforce's fiscal year ends Jan 31: FY26 ends 2026-01-31."""
    d = date.fromisoformat(end)
    fy = d.year if d.month == 1 else d.year + 1
    if not quarter:
        return f"FY{fy % 100:02d}"
    q = {4: 1, 7: 2, 10: 3, 1: 4}[d.month]
    return f"Q{q} FY{fy % 100:02d}"


def series(facts, tag, min_days, max_days):
    out = {}
    for unit in facts[tag]["units"].values():
        for v in unit:
            if "start" not in v:
                continue
            days = (date.fromisoformat(v["end"]) - date.fromisoformat(v["start"])).days
            if min_days <= days <= max_days:
                out[v["end"]] = v["val"] / 1e6  # later filings overwrite earlier ones
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="saved companyfacts JSON instead of downloading")
    ap.add_argument("--first-fy", type=int, default=2021)
    args = ap.parse_args()

    gaap = load(args.input)["facts"]["us-gaap"]
    annual, quarterly = {}, {}
    for key, tag in TAGS.items():
        for end, val in series(gaap, tag, 350, 380).items():
            if date.fromisoformat(end).year >= args.first_fy:
                annual.setdefault(fiscal_label(end), {})[key] = val
        if key in FLOW_ONLY_ANNUAL:
            continue
        q = series(gaap, tag, 80, 100)
        for end, val in q.items():
            if date.fromisoformat(end).year >= args.first_fy + 4:
                quarterly.setdefault(fiscal_label(end, True), {})[key] = val

    # Q4 is not filed separately: derive it as full year minus Q1-Q3.
    for fy, row in annual.items():
        qs = [quarterly.get(f"Q{i} {fy}") for i in (1, 2, 3)]
        if all(qs) and f"Q4 {fy}" not in quarterly:
            quarterly[f"Q4 {fy}"] = {
                k: row[k] - sum(q.get(k, 0) for q in qs) for k in row if k not in FLOW_ONLY_ANNUAL
            }

    rpo = {}
    for v in gaap["RevenueRemainingPerformanceObligation"]["units"]["USD"]:
        if v["end"].endswith("-01-31"):
            rpo[fiscal_label(v["end"])] = v["val"] / 1e9

    def qkey(k):
        q, fy = k.split()
        return (fy, q)

    out = {
        "source": URL,
        "units": {"financials": "USD millions", "rpo": "USD billions"},
        "annual": dict(sorted(annual.items())),
        "quarterly": {k: quarterly[k] for k in sorted(quarterly, key=qkey)},
        "rpo_fiscal_year_end": dict(sorted(rpo.items())),
    }
    dest = Path(__file__).resolve().parent.parent / "data" / "crm_financials.json"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
