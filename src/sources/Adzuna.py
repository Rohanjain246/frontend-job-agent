import requests
import os

ADZUNA_APP_ID  = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_API_KEY = os.getenv("ADZUNA_API_KEY", "")

# Search terms tuned for your React/TS/Next.js profile
QUERIES = [
    "react developer",
    "frontend developer typescript",
    "next.js developer",
    "react typescript remote",
]


def fetch_adzuna():
    """
    Fetches jobs from the official Adzuna API.
    Free dev tier: 1,000 calls/day — plenty for daily GitHub Actions runs.
    Sign up at: https://developer.adzuna.com/
    Covers India jobs well — good Naukri/Indeed alternative.
    """
    if not ADZUNA_APP_ID or not ADZUNA_API_KEY:
        print("Adzuna: skipping — ADZUNA_APP_ID or ADZUNA_API_KEY not set")
        return []

    jobs = []
    seen = set()

    for what in QUERIES:
        try:
            response = requests.get(
                "https://api.adzuna.com/v1/api/jobs/in/search/1",
                params={
                    "app_id":          ADZUNA_APP_ID,
                    "app_key":         ADZUNA_API_KEY,
                    "what":            what,
                    "content-type":    "application/json",
                    "results_per_page": 50,
                    "sort_by":         "date",
                },
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()

            for job in data.get("results", []):
                job_id = job.get("id", "")
                if job_id in seen:
                    continue
                seen.add(job_id)

                # Normalize to the same shape as other sources
                jobs.append({
                    "title":       job.get("title", ""),
                    "company":     job.get("company", {}).get("display_name", ""),
                    "description": job.get("description", ""),
                    "url":         job.get("redirect_url", ""),
                    "tags":        [],
                    "platform":    "Adzuna",
                })

        except requests.exceptions.Timeout:
            print(f"Adzuna timeout for query: {what}")
        except requests.exceptions.HTTPError as e:
            print(f"Adzuna HTTP {e.response.status_code} for query: {what}")
        except Exception as e:
            print(f"Adzuna error ({what}): {e}")

    print(f"Adzuna: fetched {len(jobs)} jobs across {len(QUERIES)} queries")
    return jobs
