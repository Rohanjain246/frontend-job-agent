import requests

def fetch_remoteok():
try:
response = requests.get(
"https://remoteok.com/api",
headers={
"User-Agent": "Mozilla/5.0"
},
timeout=20
)


    data = response.json()

    if isinstance(data, list):
        return data[1:]

    return []

except Exception as e:
    print("RemoteOK Error:", e)
    return []

