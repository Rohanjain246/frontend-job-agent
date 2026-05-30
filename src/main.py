print("NEW VERSION LOADED")

from sources.remoteok        import fetch_remoteok
from sources.remotive        import fetch_remotive
from sources.Jsearch         import fetch_jsearch
from sources.Adzuna          import fetch_adzuna
from sources.linkedin_public import fetch_linkedin
from notifier.sheets         import push_to_sheet
from scorer import score_job

import pandas as pd
from datetime import date
import os

jobs      = []
seen_keys = set()    # deduplicate across all sources

sources = [
    ("RemoteOK",  fetch_remoteok),
    ("Remotive",  fetch_remotive),
    ("JSearch",   fetch_jsearch),
    ("Adzuna",    fetch_adzuna),
    ("LinkedIn",  fetch_linkedin),
]

for source_name, fn in sources:
    print(f"\nChecking {source_name}...")
    jobs_data = fn()
    print(f"Found {len(jobs_data)} raw jobs from {source_name}")

    for j in jobs_data:
        score   = score_job(j)
        title   = j.get("title")   or j.get("position")     or "Unknown"
        company = j.get("company") or j.get("company_name") or "Unknown"
        url     = j.get("url")     or j.get("job_url")      or ""

        # Deduplicate across sources
        key = f"{title.lower().strip()}|{company.lower().strip()}"
        if key in seen_keys:
            continue
        seen_keys.add(key)

        if score >= 10:
            print(f"  ATS={score:>3}/100 | {title} | {company}")
            jobs.append({
                "Date":             date.today().isoformat(),
                "Company":          company,
                "Role":             title,
                "Score":            score,
                "Source":           source_name,
                "URL":              url,
                "Applied":          "",
                "ApplicationDate":  "",
                "Interview Status": "",
                "Offer":            "",
                "Notes":            "",
                # internal fields for sheets.py deduplication
                "title":            title,
                "company":          company,
                "score":            score,
                "source":           source_name,
            })

os.makedirs("reports", exist_ok=True)

EXPORT_COLS = ["Date","Company","Role","Score","Source","URL",
               "Applied","ApplicationDate","Interview Status","Offer","Notes"]

if not jobs:
    print("\nNo matching jobs found (threshold: ATS >= 10)")
    df = pd.DataFrame(columns=EXPORT_COLS)
else:
    df = pd.DataFrame(jobs)
    df = df.sort_values("Score", ascending=False).reset_index(drop=True)

# ── Save CSV (URLs are plain text — clickable in Excel/Sheets when imported) ─
df[EXPORT_COLS].to_csv("reports/jobs.csv", index=False)

# ── Print terminal summary ────────────────────────────────────────────────────
print("\n── All Matches (ATS >= 10) ─────────────────────────")
print(df[["Score","Role","Company","Source"]].head(20).to_string(index=False))

strong = df[df["Score"] >= 80]
if not strong.empty:
    print(f"\n🎯  Strong ATS Matches (80+/100) — {len(strong)} jobs:")
    print(strong[["Score","Role","Company","Source"]].to_string(index=False))
else:
    print("\nNo 80+ ATS matches today.")

print(f"\nTotal saved to reports/jobs.csv: {len(df)} jobs")

# ── Push to Google Sheets ─────────────────────────────────────────────────────
push_to_sheet(df)
