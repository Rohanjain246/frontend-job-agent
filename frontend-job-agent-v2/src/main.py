
from sources.remoteok import fetch_remoteok
from sources.remotive import fetch_remotive
from scorer import score_job
import pandas as pd

jobs=[]
for fn in [fetch_remoteok, fetch_remotive]:
    for j in fn():
        s=score_job(str(j))
        if s>=70:
            jobs.append({'score':s,'title':j.get('position') or j.get('title'),'company':j.get('company')})
df=pd.DataFrame(jobs).sort_values('score',ascending=False)
df.to_csv('reports/jobs.csv',index=False)
print(df.head())
