import json
import os

# Resolve path to resume_keywords.json relative to this file
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_KEYWORDS_PATH = os.path.join(_BASE_DIR, "resume_keywords.json")

with open(_KEYWORDS_PATH) as f:
    kw = json.load(f)

PRIMARY   = [k.lower() for k in kw.get("primary",   [])]
SECONDARY = [k.lower() for k in kw.get("secondary", [])]
EXCLUDE   = [k.lower() for k in kw.get("exclude",   [])]


def score_job(job) -> int:
    """
    Works with BOTH:
      dict  → job object from API         e.g. score_job(j)
      str   → string-cast dict from main  e.g. score_job(str(j))   ✅
    """
    if isinstance(job, dict):
        title       = (job.get("title",       "") or "").lower()
        description = (job.get("description", "") or "").lower()
        tags        = " ".join(job.get("tags", []) or []).lower()
        text        = f"{title} {description} {tags}"
    elif isinstance(job, str):
        text = job.lower()
    else:
        return 0

    for word in EXCLUDE:
        if word in text:
            return -99

    score = 0
    for word in PRIMARY:
        if word in text:
            score += 3
    for word in SECONDARY:
        if word in text:
            score += 1

    return score
