import requests

def fetch_remotive():
try:
response = requests.get(
"https://remotive.com/api/remote-jobs",
timeout=20
)

    data = response.json()

    return data.get("jobs", [])

except Exception as e:
    print("Remotive Error:", e)
    return []
