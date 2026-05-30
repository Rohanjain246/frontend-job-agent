import requests
import time
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Public search queries — no login needed, no ToS violation
SEARCHES = [
    {"keywords": "react developer",             "location": "India", "f_WT": "2"},
    {"keywords": "frontend developer typescript","location": "India", "f_WT": "2"},
    {"keywords": "next.js developer",           "location": "India", "f_WT": "2"},
    {"keywords": "react developer",             "location": "Remote","f_WT": "2"},
]


def fetch_linkedin():
    """
    Scrapes LinkedIn's PUBLIC job search results (no login, no cookies).
    This accesses only data visible to any anonymous visitor — not behind
    any login wall — which is consistent with the hiQ v. LinkedIn ruling.

    Note: LinkedIn's HTML structure can change. If this breaks, the
    fix is to update the CSS selectors below. No credentials needed.
    """
    jobs = []
    seen = set()

    for search in SEARCHES:
        try:
            response = requests.get(
                "https://www.linkedin.com/jobs/search/",
                headers=HEADERS,
                params=search,
                timeout=20,
            )

            if response.status_code == 429:
                print("LinkedIn: rate-limited — skipping remaining queries")
                break

            if response.status_code != 200:
                print(f"LinkedIn: status {response.status_code} for {search['keywords']}")
                continue

            soup = BeautifulSoup(response.text, "lxml")

            # LinkedIn public page job cards
            cards = soup.find_all("div", class_="base-card")

            # Fallback selector if LinkedIn updated their HTML
            if not cards:
                cards = soup.find_all("li", class_=lambda c: c and "result-card" in c)

            for card in cards:
                try:
                    title_el   = (card.find("h3", class_="base-search-card__title") or
                                  card.find("h3"))
                    company_el = (card.find("h4", class_="base-search-card__subtitle") or
                                  card.find("h4"))
                    link_el    = card.find("a", class_="base-card__full-link") or card.find("a")

                    title   = title_el.get_text(strip=True)   if title_el   else ""
                    company = company_el.get_text(strip=True) if company_el else ""
                    url     = link_el.get("href", "")         if link_el    else ""

                    if not title:
                        continue

                    key = f"{title.lower()}|{company.lower()}"
                    if key in seen:
                        continue
                    seen.add(key)

                    jobs.append({
                        "title":       title,
                        "company":     company,
                        "description": f"{title} at {company}",  # no full desc without login
                        "url":         url,
                        "tags":        [],
                        "platform":    "LinkedIn",
                    })

                except Exception:
                    continue

            time.sleep(2)   # be polite — avoid triggering rate limits

        except requests.exceptions.Timeout:
            print(f"LinkedIn timeout for: {search['keywords']}")
        except Exception as e:
            print(f"LinkedIn error ({search['keywords']}): {e}")

    print(f"LinkedIn: fetched {len(jobs)} public jobs")
    return jobs
