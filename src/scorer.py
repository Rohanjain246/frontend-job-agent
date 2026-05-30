import json
import os

_BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_KEYWORDS_PATH = os.path.join(_BASE_DIR, "resume_keywords.json")

with open(_KEYWORDS_PATH) as f:
    kw = json.load(f)

PRIMARY   = [k.lower() for k in kw.get("primary",   [])]
SECONDARY = [k.lower() for k in kw.get("secondary", [])]
WATCHLIST = [k.lower() for k in kw.get("watchlist", [])]
EXCLUDE   = [k.lower() for k in kw.get("exclude",   [])]


def score_job(job) -> int:
    """
    Accepts dict or str(dict) — handles both safely.

    Scoring:
      +3  per primary keyword   (react, typescript, next.js ...)
      +1  per secondary keyword (tailwind, redux, vite ...)
      +5  if company is on watchlist (stripe, vercel, razorpay ...)
      -99 if any exclude keyword found (disqualifies entirely)
    """
    if isinstance(job, dict):
        title       = (job.get("title",       "") or job.get("position", "") or "").lower()
        description = (job.get("description", "") or "").lower()
        company     = (job.get("company", "")     or job.get("company_name", "") or "").lower()
        tags        = " ".join(job.get("tags", []) or []).lower()
        text        = f"{title} {description} {tags}"
    elif isinstance(job, str):
        text    = job.lower()
        company = text          # company name is embedded in str(dict) too
    else:
        return 0

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

    # Watchlist bonus — float dream companies to the top
    for name in WATCHLIST:
        if name in company:
            score += 5
            break

    return score
