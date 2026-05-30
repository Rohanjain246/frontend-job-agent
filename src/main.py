print("NEW VERSION LOADED")
from sources.remoteok import fetch_remoteok
from sources.remotive import fetch_remotive
from scorer import score_job
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
        score = score_job(str(j))

        title = j.get("position") or j.get("title") or "Unknown"
        company = j.get("company") or j.get("company_name") or "Unknown"

        if score > 0:
            print(f"Score={score} | {title} | {company}")

        if score >= 25:
            jobs.append(
                {
                    "source": source_name,
                    "score": score,
                    "title": title,
                    "company": company,
                }
            )

os.makedirs("reports", exist_ok=True)

if not jobs:
    print("No matching jobs found")
    df = pd.DataFrame(columns=["source", "score", "title", "company"])
else:
    df = pd.DataFrame(jobs)

if not df.empty and "score" in df.columns:
    df = df.sort_values("score", ascending=False)

df.to_csv("reports/jobs.csv", index=False)

print("\nTop Results:")
print(df.head(20))

print(f"\nSaved {len(df)} jobs to reports/jobs.csv")
