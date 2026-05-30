import requests

def fetch_yc_jobs():
    try:
        response = requests.get(
            "https://www.ycombinator.com/jobs",
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        # Placeholder for now
        # YC does not provide a simple public API
        # We will improve this later

        return []

    except Exception as e:
        print("YC Error:", str(e))
        return []   
