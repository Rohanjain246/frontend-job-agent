import json
import os

# Resolve path to resume_keywords.json relative to this file,
# so it works whether you run from repo root or src/
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_KEYWORDS_PATH = os.path.join(_BASE_DIR, "resume_keywords.json")

with open(_KEYWORDS_PATH) as f:
    kw = json.load(f)          # ← FIXED: was at column 0 (IndentationError)

PRIMARY   = [k.lower() for k in kw.get("primary",   [])]
SECONDARY = [k.lower() for k in kw.get("secondary", [])]
EXCLUDE   = [k.lower() for k in kw.get("exclude",   [])]


def score_job(job: dict) -> int:
    """
    Score a job dict from the Remotive API.

    Scoring rules:
      +3 per primary keyword match   (title or description)
      +1 per secondary keyword match (title or description)
      -99 if any exclude keyword is found  (effectively disqualifies)

    Returns an integer score. Higher = better match.
    """
    title       = (job.get("title",       "") or "").lower()
    description = (job.get("description", "") or "").lower()
    tags        = " ".join(job.get("tags", []) or []).lower()
    text        = f"{title} {description} {tags}"

    # Hard disqualifiers
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
