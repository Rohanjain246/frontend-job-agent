import requests

def fetch_remoteok():
    try:                                    # ← indented inside function
        response = requests.get(
            "https://remoteok.com/api",     # ← indented inside try
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )
        data = response.json()
        if isinstance(data, list):
            return data[1:]
        return []
    except Exception as e:                  # ← same level as try
        print("RemoteOK Error:", e)
        return []
