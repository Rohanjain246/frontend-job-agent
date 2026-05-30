
import json
kw=json.load(open('resume_keywords.json'))
def score_job(text):
    text=text.lower()
    score=0
    for k in kw['primary']:
        if k in text: score+=15
    for k in kw['secondary']:
        if k in text: score+=5
    return min(score,100)
