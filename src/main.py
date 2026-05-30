print("NEW VERSION LOADED")

from sources.remoteok import fetch_remoteok
from sources.remotive import fetch_remotive
from scorer import score_job
from email_report import send_email_report
import pandas as pd
import os

jobs = []

sources = [
    ("RemoteOK", fetch_remoteok),
    ("Remotive", fetch_remotive),
]

for source_name, fn in sources:
    print(f"\nChecking {source_name}...\n")
    jobs_data = fn()
    print(f"Found {len(jobs_data)} jobs")

    for j in jobs_data:
        score = score_job(j)              # ✅ FIXED: was score_job(str(j))
                                          #    str(j) passes a raw string like
                                          #    "{'title': ...}" which breaks
                                          #    scorer's .get() calls on the dict
        title   = j.get("position") or j.get("title")        or "Unknown"
        company = j.get("company")  or j.get("company_name") or "Unknown"

        if score > 0:
            print(f"Score={score} | {title} | {company}")

        if score >= 5:                    # ✅ FIXED: was 25 — unreachable with
                                          #    typical keyword hits (+3 primary,
                                          #    +1 secondary). Lowered to 5 so
                                          #    at least 1 strong primary match
                                          #    qualifies. Adjust to taste.
            jobs.append({
                "source":  source_name,
                "score":   score,
                "title":   title,
                "company": company,
            })

os.makedirs("reports", exist_ok=True)

if not jobs:
    print("\nNo matching jobs found")
    df = pd.DataFrame(columns=["source", "score", "title", "company"])
else:
    df = pd.DataFrame(jobs)

if not df.empty and "score" in df.columns:
    df = df.sort_values("score", ascending=False)

df.to_csv("reports/jobs.csv", index=False)
report_lines = []

for _, row in df.head(20).iterrows():
    report_lines.append(
        f"{row['title']} | {row['company']} | Score {row['score']}"
    )

report_text = "\n".join(report_lines)

send_email_report(report_text)
print("\nTop Results:")
print(df.head(20))
print(f"\nSaved {len(df)} jobs to reports/jobs.csv")
