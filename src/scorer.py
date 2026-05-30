import json
import os

# Get path to resume_keywords.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYWORDS_PATH = os.path.join(BASE_DIR, "resume_keywords.json")

with open(KEYWORDS_PATH, "r", encoding="utf-8") as f:
    kw = json.load(f)

PRIMARY = [k.lower() for k in kw.get("primary", [])]
SECONDARY = [k.lower() for k in kw.get("secondary", [])]
EXCLUDE = [k.lower() for k in kw.get("exclude", [])]

def score_job(job):
    if isinstance(job, dict):
        title = str(job.get("title", "")).lower()
        description = str(job.get("description", "")).lower()
        tags = " ".join(job.get("tags", []))
        text = f"{title} {description} {tags}".lower()
    else:
        text = str(job).lower()

    for word in EXCLUDE:
        if word in text:
            return -999

    must_have = [
        "react",
        "frontend",
        "javascript",
        "typescript",
        "next.js"
    ]

    if not any(word in text for word in must_have):
        return 0

    score = 0

    for word in PRIMARY:
        if word in text:
            score += 20

    for word in SECONDARY:
        if word in text:
            score += 10

    return min(score, 100)
