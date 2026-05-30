
import requests
def fetch_remotive():
    try:return requests.get('https://remotive.com/api/remote-jobs',timeout=20).json().get('jobs',[])
    except:return []
