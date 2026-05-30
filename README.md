# Frontend Job Agent V2

Production-style scaffold with GitHub Actions that automatically fetches, filters, and reports frontend job listings.

## What It Does

- Fetches remote frontend jobs from **Remotive API**
- Filters jobs based on keywords from `resume_keywords.json`
- Sends a daily email digest report
- Logs matches to a **Google Sheet**
- Runs automatically via **GitHub Actions**

## Project Structure

```
frontend-job-agent/
├── .github/workflows/     # GitHub Actions CI schedule
├── src/
│   └── sources/
│       └── remotive.py    # Remotive API fetcher
├── .env.example           # Environment variable template
├── requirements.txt       # Python dependencies
├── resume_keywords.json   # Job filter keywords
└── README.md
```

## Setup

### 1. Clone & Install
```bash
git clone https://github.com/Rohanjain246/frontend-job-agent.git
cd frontend-job-agent
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

Required variables in `.env`:
- `EMAIL_USER` — Gmail address for sending reports
- `EMAIL_PASSWORD` — Gmail App Password (not your login password)
- `REPORT_RECEIVER` — Email address to receive job digests
- `GOOGLE_SHEET_ID` — Google Sheet ID for logging matches

### 3. Set GitHub Secrets
Add the same variables as **Repository Secrets** in:
`Settings → Secrets and variables → Actions`

## Customizing Keywords

Edit `resume_keywords.json`:
- **primary** — must-match terms (React, TypeScript, etc.)
- **secondary** — nice-to-have terms (Tailwind, Redux, etc.)
- **exclude** — terms that disqualify a job

## Running Locally
```bash
python -m src.main
```
