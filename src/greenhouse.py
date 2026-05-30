import requests

GREENHOUSE_BOARDS = ["stripe", "vercel", "atlassian", "browserstack"]


def fetch_greenhouse_jobs():
    jobs = []

    for board in GREENHOUSE_BOARDS:
        try:
            # Add ?content=true to get departments, offices, and full descriptions
            url = (
                f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
            )

            response = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                },  # Good practice to include User-Agent
                timeout=20,
            )

            # Raise an error for bad status codes (e.g., 404, 500)
            response.raise_for_status()

            data = response.json()

            for job in data.get("jobs", []):
                # Extract departments and offices if needed
                departments = [d.get("name") for d in job.get("departments", [])]
                offices = [o.get("name") for o in job.get("offices", [])]

                jobs.append(
                    {
                        "title": job.get("title"),
                        "company": board,
                        "url": job.get("absolute_url"),
                        "description": job.get(
                            "content", ""
                        ),  # Now available because ?content=true
                        "departments": departments,
                        "offices": offices,
                    }
                )

        except Exception as e:
            print(f"Greenhouse {board} error:", str(e))

    return jobs
