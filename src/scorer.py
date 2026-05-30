import json
import os

_BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_KEYWORDS_PATH = os.path.join(_BASE_DIR, "resume_keywords.json")

with open(_KEYWORDS_PATH) as f:
    kw = json.load(f)

CORE_TECH  = [k.lower() for k in kw.get("core_tech",  [])]
ROLE_TERMS = [k.lower() for k in kw.get("role_terms", [])]
SKILLS     = [k.lower() for k in kw.get("skills",     [])]
WATCHLIST  = [k.lower() for k in kw.get("watchlist",  [])]
EXCLUDE    = [k.lower() for k in kw.get("exclude",    [])]

# ── ATS Score breakdown (max 100) ────────────────────────────────────────────
#
#  Core tech match   0–45  (react, typescript, next.js, javascript — 15 pts each)
#  Role match        0–25  (25 if in title, 15 if in description only)
#  Skills match      0–20  (tailwind, redux, graphql etc — 3 pts each, capped 20)
#  Watchlist bonus   0–10  (stripe, vercel, razorpay etc)
#  ─────────────────────────
#  Total             0–100
#
#  Threshold in main.py: >= 10 → goes to CSV
#                        >= 80 → goes to "Strong Matches" tab in Sheets


def score_job(job) -> int:
    if isinstance(job, dict):
        title   = (job.get("title",       "") or job.get("position", "") or "").lower()
        desc    = (job.get("description", "") or "").lower()
        company = (job.get("company",     "") or job.get("company_name", "") or "").lower()
        tags    = " ".join(job.get("tags", []) or []).lower()
        text    = f"{title} {desc} {tags}"
    elif isinstance(job, str):
        text    = job.lower()
        title   = text
        company = text
    else:
        return 0

    # Hard disqualifiers — return 0 so they are filtered out cleanly
    for word in EXCLUDE:
        if word in text:
            return 0

    # ── Core tech (0–45) ─────────────────────────────────────────────────────
    tech_hits  = sum(1 for w in CORE_TECH if w in text)
    tech_score = min(tech_hits * 15, 45)

    # ── Role match (0–25) ────────────────────────────────────────────────────
    if any(r in title for r in ROLE_TERMS):
        role_score = 25          # exact role in title → strongest signal
    elif any(r in text for r in ROLE_TERMS):
        role_score = 15          # role mentioned in description
    else:
        role_score = 0

    # ── Skills (0–20) ────────────────────────────────────────────────────────
    skill_hits  = sum(1 for s in SKILLS if s in text)
    skill_score = min(skill_hits * 3, 20)

    # ── Watchlist bonus (0–10) ───────────────────────────────────────────────
    watchlist_bonus = 10 if any(n in company for n in WATCHLIST) else 0

    total = tech_score + role_score + skill_score + watchlist_bonus
    return min(total, 100)
