import requests


def fetch_remotive():
    """
    Fetches frontend job listings from the Remotive API.
    Returns a list of job dicts, or [] on failure.
    """
    try:
        response = requests.get(
            "https://remotive.com/api/remote-jobs?category=software-dev",
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )
        response.raise_for_status()  # raises HTTPError for 4xx/5xx
        data = response.json()

        if isinstance(data, dict) and "jobs" in data:
            return data["jobs"]

        return []

    except requests.exceptions.Timeout:
        print("Remotive Error: Request timed out")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"Remotive Error: HTTP {e.response.status_code}")
        return []
    except Exception as e:
        print(f"Remotive Error: {e}")
        return []
