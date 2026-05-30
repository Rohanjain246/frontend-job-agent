print("NEW VERSION LOADED")

from sources.remoteok        import fetch_remoteok
from sources.remotive        import fetch_remotive
from sources.Jsearch         import fetch_jsearch
from sources.Adzuna          import fetch_adzuna
from sources.linkedin_public import fetch_linkedin
from scorer import score_job

import pandas as pd
import os

jobs = []

sources = [
    ("RemoteOK",  fetch_remoteok),
    ("Remotive",  fetch_remotive),
    ("JSearch",   fetch_jsearch),      # LinkedIn + Indeed + Glassdoor + Naukri
    ("Adzuna",    fetch_adzuna),       # India-focused official API
    ("LinkedIn",  fetch_linkedin),     # Public search, no login
]

seen_titles = set()   # deduplicate across all sources

for source_name, fn in sources:
    print(f"\nChecking {source_name}...")
    jobs_data = fn()
    print(f"Found {len(jobs_data)} jobs from {source_name}")

    for j in jobs_data:
        score = score_job(j)           # pass dict directly — scorer handles it

        title   = j.get("title")   or j.get("position")     or "Unknown"
        company = j.get("company") or j.get("company_name") or "Unknown"
        url     = j.get("url")     or j.get("job_url")      or ""

        # deduplicate by title+company across all sources
        dedup_key = f"{title.lower()}|{company.lower()}"
        if dedup_key in seen_titles:
            continue
        seen_titles.add(dedup_key)

        if score > 0:
            print(f"  Score={score:>3} | {title} | {company}")

        if score >= 5:                 # >=5 = at least 1 strong primary keyword
            jobs.append({
                "source":  source_name,
                "score":   score,
                "title":   title,
                "company": company,
                "url":     url,
            })

os.makedirs("reports", exist_ok=True)

if not jobs:
    print("\nNo matching jobs found above threshold")
    df = pd.DataFrame(columns=["source", "score", "title", "company", "url"])
else:
    df = pd.DataFrame(jobs)

if not df.empty and "score" in df.columns:
    df = df.sort_values("score", ascending=False).reset_index(drop=True)

df.to_csv("reports/jobs.csv", index=False)

print("\n-- Top Results --")
print(df[["score", "title", "company", "source"]].head(20).to_string(index=False))
print(f"\nSaved {len(df)} jobs to reports/jobs.csv")
