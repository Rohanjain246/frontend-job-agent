import requests


def fetch_remoteok():
    """
    Fetches remote job listings from the RemoteOK API.
    Returns a list of job dicts, or [] on failure.
    Note: The first item in the response is metadata, so we skip it with [1:]
    """
    try:
        response = requests.get(
            "https://remoteok.com/api",
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return data[1:]  # index 0 is a metadata/legal notice dict

        return []

    except requests.exceptions.Timeout:
        print("RemoteOK Error: Request timed out")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"RemoteOK Error: HTTP {e.response.status_code}")
        return []
    except Exception as e:
        print(f"RemoteOK Error: {e}")
        return []
