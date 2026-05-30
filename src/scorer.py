import json

with open("resume_keywords.json", "r", encoding="utf-8") as f:
kw = json.load(f)

def score_job(text):
text = text.lower()
score = 0

for k in kw["primary"]:
    if k.lower() in text:
        score += 15

for k in kw["secondary"]:
    if k.lower() in text:
        score += 5

return min(score, 100)
