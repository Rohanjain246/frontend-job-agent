
import requests
def fetch_remoteok():
    try:return requests.get('https://remoteok.com/api',timeout=20).json()
    except:return []
