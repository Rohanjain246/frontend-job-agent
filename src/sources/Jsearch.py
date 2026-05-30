import requests
import os

JSEARCH_KEY = os.getenv("JSEARCH_API_KEY", "")

# Queries tuned for React/TypeScript/Next.js frontend roles
QUERIES = [
    "react developer remote",
    "frontend developer typescript remote",
    "next.js engineer remote",
    "react typescript frontend india",
]


def fetch_jsearch():
    """
    Fetches jobs from JSearch (RapidAPI) — aggregates LinkedIn, Indeed,
    Glassdoor, Naukri legally via one API. Free tier: 200 calls/month.
    Sign up at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
    """
    if not JSEARCH_KEY:
        print("JSearch: skipping — JSEARCH_API_KEY not set")
        return []

    jobs = []
    seen = set()

    for query in QUERIES:
        try:
            response = requests.get(
                "https://jsearch.p.rapidapi.com/search",
                headers={
                    "X-RapidAPI-Key": JSEARCH_KEY,
                    "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
                },
                params={
                    "query": query,
                    "page": "1",
                    "num_pages": "1",
                    "employment_types": "FULLTIME",
                    "date_posted": "today",
                },
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()

            for job in data.get("data", []):
                job_id = job.get("job_id", "")
                if job_id in seen:
                    continue
                seen.add(job_id)

                # Normalize to the same shape as remoteok/remotive
                jobs.append({
                    "title":       job.get("job_title", ""),
                    "company":     job.get("employer_name", ""),
                    "description": job.get("job_description", ""),
                    "url":         job.get("job_apply_link", ""),
                    "tags":        job.get("job_required_skills") or [],
                    "platform":    job.get("job_publisher", "JSearch"),
                })

        except requests.exceptions.Timeout:
            print(f"JSearch timeout for query: {query}")
        except requests.exceptions.HTTPError as e:
            print(f"JSearch HTTP {e.response.status_code} for query: {query}")
        except Exception as e:
            print(f"JSearch error ({query}): {e}")

    print(f"JSearch: fetched {len(jobs)} jobs across {len(QUERIES)} queries")
    return jobs
